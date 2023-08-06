# Copyright 2019 Katteli Inc.
# TestFlows.com Open-Source Software Testing Framework (http://testflows.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import sys
import time
import random
import inspect
import builtins
import operator
import functools
import tempfile
import threading
import textwrap
import importlib

from contextlib import ExitStack, contextmanager
from collections import namedtuple

import testflows.settings as settings

from .templog import filename as templog_filename
from .exceptions import DummyTestException, ResultException, TestIteration, DescriptionError, TestRerunIndividually
from .flags import Flags, SKIP, TE, FAIL_NOT_COUNTED, ERROR_NOT_COUNTED, NULL_NOT_COUNTED, MANDATORY, MANUAL, AUTO
from .flags import XOK, XFAIL, XNULL, XERROR, XRESULT
from .flags import EOK, EFAIL, EERROR, ESKIP, ERESULT
from .flags import CFLAGS, PAUSE_BEFORE, PAUSE_AFTER
from .testtype import TestType, TestSubType
from .objects import get, Null, OK, Fail, Skip, Error, PassResults, Argument, Attribute, Requirement, ArgumentParser
from .objects import RepeatTest, ExamplesTable, Specification
from .objects import Secret
from .constants import name_sep, id_sep
from .io import TestIO, LogWriter
from .name import join, depth, match, absname, split, isabs
from .funcs import current, top, previous, main, exception, pause, _set_current_top_previous, result, input
from .init import init
from .cli.arg.parser import ArgumentParser as ArgumentParserClass
from .cli.arg.common import epilog as common_epilog
from .cli.arg.exit import ExitWithError, ExitException
from .cli.arg.type import key_value as key_value_type, repeat as repeat_type, tags_filter as tags_filter_type
from .cli.arg.type import logfile as logfile_type, rsa_private_key_pem_file as rsa_private_key_pem_file_type
from .cli.text import danger, warning
from .exceptions import exception as get_exception
from .filters import The, TheTags
from .utils.sort import human as human_sort
from .transform.log.pipeline import ResultsLogPipeline

try:
    import testflows.database as database_module
except:
    database_module = None

def run_generator(r):
    """Run generator.
    """
    return next(r)

class DummyTest(object):
    """Base class for dummy tests.
    """
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        def dummy(*args, **kwargs):
            pass

        self.trace = sys.gettrace()
        sys.settrace(dummy)
        sys._getframe(1).f_trace = self.__skip__

    def __skip__(self, *args):
        sys.settrace(self.trace)
        raise DummyTestException()

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if isinstance(exception_value, DummyTestException):
            return True

class Context(object):
    """Test context.
    """
    def __init__(self, parent, state=None):
        self._parent = parent
        self._state = get(state, {})
        self._cleanups = []

    @property
    def parent(self):
        return self._parent

    def cleanup(self, func, *args, **kwargs):
        def func_wrapper():
            func(*args, **kwargs)
        self._cleanups.append(func_wrapper)

    def _cleanup(self):
        exc_type, exc_value, exc_traceback = None, None, None
        for func in reversed(self._cleanups):
            try:
                func()
            except StopIteration:
                pass
            except (Exception, KeyboardInterrupt) as e:
                if not exc_value:
                    exc_type, exc_value, exc_traceback = sys.exc_info()
        return exc_type, exc_value, exc_traceback

    def __getattr__(self, name):
        try:
            if name.startswith('_'):
                return self.__dict__[name]
        except KeyError:
            raise AttributeError(name) from None

        curr = self
        while True:
            try:
                return curr._state[name]
            except KeyError:
                if curr._parent:
                    curr = curr._parent
                    continue
                raise AttributeError(name) from None

    def __setattr__(self, name, value):
        if name.startswith('_'):
            self.__dict__[name] = value
        else:
            self._state[name] = value

    def __delattr__(self, name):
        try:
            del self._state[name]
        except KeyError:
            raise AttributeError(name) from None

    def __contains__(self, name):
        if name.startswith('_'):
            return name in self.__dict__

        curr = self
        while True:
            if name in curr._state:
                return True
            if curr._parent:
                curr = curr._parent
            else:
                return False

class TestBase(object):
    """Base class for all the tests.

    :param name: name
    :param flags: flags
    :param parent: parent name
    :param only: tests to run
    :param start: name of the starting test
    :param end: name of the last test
    """
    uid = None
    tags = set()
    attributes = []
    requirements = []
    specifications = []
    examples = None
    name = None
    description = None
    node = None
    map = []
    flags = Flags()
    name_sep = "."
    type = TestType.Test
    subtype = None

    def __init__(self, name=None, flags=None, cflags=None, type=None, subtype=None,
                 uid=None, tags=None, attributes=None, requirements=None, specifications=None,
                 examples=None, description=None, parent=None,
                 xfails=None, xflags=None, only=None, skip=None,
                 start=None, end=None, only_tags=None, skip_tags=None,
                 args=None, id=None, node=None, map=None, context=None,
                 repeat=None, private_key=None, setup=None):

        self.lock = threading.Lock()

        if current() is None:
            if top() is not None:
                raise RuntimeError("only one top level test is allowed")
            top(self)
            # flag to indicate if main test called init
            self._init= False

        current_test = current()

        self.io = None
        self.name = name
        if self.name is None:
            raise TypeError("name must be specified")
        self.child_count = 0
        self.start_time = time.time()
        self.parent = parent
        self.id = get(id, [settings.test_id])
        self.node = get(node, self.node)
        self.map = get(map, list(self.map))
        self.type = get(type, self.type)
        self.subtype = get(subtype, self.subtype)
        self.context = get(context, current_test.context if current_test and self.type < TestType.Iteration else (Context(current_test.context if current_test else None)))
        self.tags = tags
        self.specifications = {s.name: s for s in [Specification(*r) for r in get(specifications, list(self.specifications))]}
        self.requirements = {r.name: r for r in [Requirement(*r) for r in get(requirements, list(self.requirements))]}
        self.attributes = {a.name: a for a in [Attribute(*a) for a in get(attributes, list(self.attributes))]}
        self.args = {k: Argument(k, v) for k,v in get(args, {}).items()}
        self.description = get(description, self.description)
        self.examples = get(examples, get(self.examples, ExamplesTable()))
        if not isinstance(self.examples, ExamplesTable):
            self.examples = ExamplesTable(*self.examples)
        self.result = Null(test=self.name)
        if flags is not None:
            self.flags = Flags(flags)
        if self.subtype in [TestSubType.Given, TestSubType.Finally]:
            self.flags |= MANDATORY
        self.cflags = Flags(cflags) | (self.flags & CFLAGS)
        self.uid = get(uid, self.uid)
        if self.uid is not None:
            self.uid = str(self.uid)
        self.xfails = get(xfails, None)
        self.xflags = get(xflags, None)
        self.only = get(only, None)
        self.skip = get(skip, None)
        self.start = get(start, None)
        self.end = get(end, None)
        self.only_tags = get(only_tags, None)
        self.skip_tags = get(skip_tags, None)
        self.repeat = get(repeat, None)
        self.private_key = get(private_key, None)
        self.caller_test = None
        self.setup = get(setup, None)
        if self.setup is not None:
            if isinstance(self.setup, (TestDecorator, TestDefinition)):
                pass
            elif inspect.isfunction(self.setup):
                self.setup = functools.partial(self.setup, self=self)
            else:
                raise TypeError(f"'{self.setup}' is not a valid test type")

    @classmethod
    def make_name(cls, name, parent=None, args=None, format=True):
        """Make full name.

        :param name: name
        :param parent: parent name
        :param args: arguments to the test
        """
        if args is None:
            args = dict()
        try:
            name = str(name) if name is not None else cls.name
            if name and format:
                name = name.format(**{"$cls": cls}, **args)
        except Exception as exc:
            raise NameError(f"can't format '{name}' using {args} {str(exc)}") from None
        if name is None:
            raise TypeError("name must be specified")
        # '/' is not allowed just like in Unix file names
        # so convert any '/' to U+2215 division slash
        name = name.replace(name_sep, "\u2215")
        return join(get(parent, name_sep), name)

    @classmethod
    def make_description(cls, description, args, format=True):
        if args is None:
            args = dict()
        try:
            description = str(description) if description is not None else None
            if description and format:
                description = description.format(**{"$cls": cls}, **args)
        except Exception as exc:
            raise DescriptionError(f"can't format '{description}' using {args} {str(exc)}") from None
        return description

    @classmethod
    def make_tags(cls, tags):
        return {str(tag) for tag in set(get(tags, cls.tags))}

    def _enter(self):
        if self is not top():
            if self.flags & MANUAL and not self.flags & SKIP and self.type >= TestType.Test:
                pause()

        self.io = TestIO(self)

        if top() is self:
            self._init = init()
            self.io.output.protocol()
            self.io.output.version()

            self.attributes.update({
                    arg.name: Attribute(name=arg.name, value=arg.value, type=arg.type, group=arg.group, uid=arg.uid)
                    for arg in self.args.values()
                })
            self.args = {}

        self.io.output.test_message()

        if self.flags & PAUSE_BEFORE and not self.flags & SKIP:
            pause()

        self.caller_test = current()
        current(self)

        if self.flags & SKIP:
            raise Skip("skip flag set", test=self.name)

        if self.setup is not None:
            r = self.setup()
            if inspect.isgenerator(r):
                res = next(r)
                self.context.cleanup(run_generator, r)

        return self

    def _exit(self, exc_type, exc_value, exc_traceback):
        if not self.io:
            return False

        if top() is self and not self._init:
            return False

        def process_exception(exc_type, exc_value, exc_traceback):
            if isinstance(exc_value, ResultException):
                self.result = self.result(exc_value)
            elif isinstance(exc_value, AssertionError):
                exception(exc_type, exc_value, exc_traceback, test=self)
                self.result = self.result(Fail(exc_type.__name__ + "\n" + get_exception(exc_type, exc_value, exc_traceback), test=self.name))
            else:
                exception(exc_type, exc_value, exc_traceback, test=self)
                result = Error(exc_type.__name__ + "\n" + get_exception(exc_type, exc_value, exc_traceback), test=self.name)
                self.result = self.result(result)

        try:
            if exc_value is not None:
                process_exception(exc_type, exc_value, exc_traceback)
            else:
                if isinstance(self.result, Null) and self.flags & MANUAL and not self.flags & SKIP:
                    try:
                        input(result)
                    except Exception:
                        process_exception(*sys.exc_info())
                elif isinstance(self.result, Null):
                    self.result = self.result(OK(test=self.name))
        finally:
            try:
                if self.type >= TestType.Iteration:
                    if self.context._cleanups:
                        try:
                            with Finally("I clean up"):
                                cleanup_exc_type, cleanup_exc_value, cleanup_exc_traceback = self.context._cleanup()
                                if cleanup_exc_value is not None:
                                    raise cleanup_exc_value.with_traceback(cleanup_exc_traceback)
                        except Exception:
                            if not exc_value:
                                process_exception(*sys.exc_info())
            finally:
                current(self.caller_test, set_value=True)
                previous(self)
                self._apply_eresult_flags()
                self._apply_xresult_flags()
                self._apply_xfails()
                self.io.output.result(self.result)

                if top() is self:
                    self.io.output.stop()
                    self.io.close(final=True)
                else:
                    self.io.close()

            if self.flags & PAUSE_AFTER and not self.flags & SKIP:
                pause()

        return True

    def _apply_eresult_flags(self):
        """Apply eresult flags to self.result.
        """
        if not ERESULT in self.flags:
            return

        message_template = f"{self.result.message + ', ' if self.result.message else ''}{self.result} result is converted to %(result)s because %(flag)s flag set"

        if EOK in self.flags:
            if not isinstance(self.result, OK):
                self.result = self.result(Fail(message_template % dict(result="Fail", flag="EOK")))

        if EFAIL in self.flags:
            if not isinstance(self.result, Fail):
                self.result = self.result(Fail(message_template % dict(result="Fail", flag="EFAIL")))
            else:
                self.result = self.result(OK(message_template % dict(result="OK", flag="EFAIL")))

        if EERROR in self.flags:
            if not isinstance(self.result, Error):
                self.result = self.result(Fail(message_template % dict(result="Fail", flag="EERROR")))
            else:
                self.result = self.result(OK(message_template % dict(result="OK", flag="EERROR")))

        if ESKIP in self.flags:
            if not isinstance(self.result, Skip):
                self.result = self.result(Fail(message_template % dict(result="Fail", flag="ESKIP")))
            else:
                self.result = self.result(OK(message_template% dict(result="OK", flag="ESKIP")))

    def _apply_xresult_flags(self):
        """Apply xresult flags to self.result.
        """
        if not XRESULT in self.flags:
            return

        if XOK in self.flags and isinstance(self.result, OK):
            self.result = self.result.xout("XOK flag set")

        if XFAIL in self.flags and isinstance(self.result, Fail):
            self.result = self.result.xout("XFAIL flag set")

        if XERROR in self.flags and isinstance(self.result, Error):
            self.result = self.result.xout("XERROR flag set")

        if XNULL in self.flags and isinstance(self.result, Null):
            self.result = self.result.xout("XNULL flag set")

    def _apply_xfails(self):
        """Apply xfails to self.result.
        """
        if not self.xfails:
            return

        for pattern, xouts in self.xfails.items():
            if match(self.name, pattern):
                for xout in xouts:
                    result, reason = xout
                    if isinstance(self.result, result):
                        self.result = self.result.xout(reason)

    def bind(self, func):
        """Bind function to the current test.

        :param func: function that takes an instance of test
            as the argument named 'test'
        :return: partial function with the 'test' argument set to self
        """
        return functools.partial(func, test=self)

    def message_io(self, name=""):
        """Return an instance of test's message IO
        used to write messages using print() method
        or other methods that takes a file-like
        object.

        Note: only write() and flush() methods
        are supported.

        :param name: name of the stream, default: None
        """
        return self.io.message_io(name=name)

epilog = """
option values:

pattern
  used to match test names using a unix-like file path pattern that supports wildcards
    '/' path level separator
    '*' matches any zero or more characters including '/' path level separator
    '?' matches any single character
    '[seq]' matches any character in seq
    '[!seq]' matches any character not in seq
    ':' matches any one or more characters but not including '/' path level separator
  for a literal match, wrap the meta-characters in brackets where '[?]' matches the character '?'

type
  test type either 'test','suite','module','scenario', or 'feature'

""" + common_epilog()


def cli_argparser(kwargs, argparser=None):
    """Command line argument parser.

    :argparser: test specific argument parser
    :return: argument parser
    """
    description = kwargs.get("description")
    if description is not None:
        description = str(description)

    main_parser = ArgumentParserClass(
        prog=sys.argv[0],
        description=description,
        description_prog="Test - Framework",
        epilog=epilog
    )

    if argparser:
        argparser(main_parser.add_argument_group('test arguments'))

    parser = main_parser.add_argument_group("common arguments")

    parser.add_argument("--name", dest="_name", metavar="name",
                        help="test run name", type=str, required=False)
    parser.add_argument("--tag", dest="_tags", metavar="value", nargs="+",
                        help="test run tags", type=str, required=False)
    parser.add_argument("--attr", dest="_attrs", metavar="name=value", nargs="+",
                        help="test run attributes", type=key_value_type, required=False)
    parser.add_argument("--only", dest="_only", metavar="pattern", nargs="+",
                        help="run only selected tests", type=str, required=False)
    parser.add_argument("--skip", dest="_skip", metavar="pattern",
                        help="skip selected tests", type=str, nargs="+", required=False)
    parser.add_argument("--start", dest="_start", metavar="pattern", nargs=1,
                        help="start at the selected test", type=str, required=False)
    parser.add_argument("--end", dest="_end", metavar="pattern", nargs=1,
                        help="end at the selected test", type=str, required=False)
    parser.add_argument("--only-tags", dest="_only_tags",
                        help="run only tests with selected tags",
                        type=tags_filter_type, metavar="type:tag,...", nargs="+", required=False)
    parser.add_argument("--skip-tags", dest="_skip_tags",
                        help="skip tests with selected tags",
                        type=tags_filter_type, metavar="type:tag,...", nargs="+", required=False)
    parser.add_argument("--pause-before", dest="_pause_before", metavar="pattern", nargs="+",
                        help="pause before executing selected tests", type=str, required=False)
    parser.add_argument("--pause-after", dest="_pause_after", metavar="pattern", nargs="+",
                        help="pause after executing selected tests", type=str, required=False)
    parser.add_argument("--random", dest="_random_order", action="store_true",
                        help="randomize order of auto loaded tests", required=False)
    parser.add_argument("--debug", dest="_debug", action="store_true",
                        help="enable debugging mode", default=False)
    parser.add_argument("--no-colors", dest="_no_colors", action="store_true",
                        help="disable terminal color highlighting", default=False)
    parser.add_argument("--id", metavar="id", dest="_id", type=str, help="custom test id")
    parser.add_argument("-o", "--output", dest="_output", metavar="format", type=str,
                        choices=["new-fails", "fails", "classic", "slick", "nice", "quiet", "short", "manual", "dots", "raw"], default="nice",
                        help="""stdout output format, choices are: ['new-fails','fails','classic','slick','nice','short','manual','dots','quiet','raw'],
                            default: 'nice'""")
    parser.add_argument("-l", "--log", dest="_log", metavar="file", type=str,
                        help="path to the log file where test output will be stored, default: uses temporary log file")
    parser.add_argument("--show-skipped", dest="_show_skipped", action="store_true",
                        help="show skipped tests, default: False", default=False)
    parser.add_argument("--repeat", dest="_repeat",
                        help=("number of times to repeat a test until it either fails or passes.\n"
                              "Where `pattern` is a test name pattern, "
                              "`number` is a number times to repeat the test, "
                              "`until` is either {'pass', 'fail', 'complete'} (default: 'fail')"),
                        type=repeat_type, metavar="pattern,number[,until]]", nargs="+", required=False)
    parser.add_argument("-r", "--reference", dest="_reference", metavar="log", type=logfile_type("r", encoding="utf-8"),
                        help="reference log file")

    choices = ["fails", "passes", "xouts", "ok", "fail", "error", "null",
               "xok", "xfail", "xerror", "xnull", "skip"]
    parser.add_argument("--rerun", dest="_rerun", metavar="result", type=str,
                        choices=choices, nargs="+",
                        help=("rerun tests in the --reference log file.\n"
                              f"Where `result` is either {choices}"))
    parser.add_argument("--individually", dest="_individually", action="store_true", default=False,
                        help="if --rerun is specified then rerun tests in the --reference log file individually.")

    parser.add_argument("--private-key", dest="_private_key", metavar="file", type=rsa_private_key_pem_file_type,
        help="RSA private key PEM file that can be used to encrypt secrets.")

    if database_module:
        database_module.argparser(parser)

    return main_parser

def parse_cli_args(kwargs, parser):
    """Parse command line arguments.

    :parser: argument parser
    :return: parsed known arguments
    """
    debug_processed = False

    try:
        args, unknown = parser.parse_known_args()
        args = vars(args)

        if args.get("_name"):
            kwargs["name"] = args.pop("_name")

        if args.get("_debug"):
            settings.debug = True
            args.pop("_debug")

        debug_processed = True

        if args.get("_no_colors"):
            settings.no_colors = True
            args.pop("_no_colors")

        if unknown:
            raise ExitWithError(f"unknown argument {unknown}")

        if args.get("_id"):
            settings.test_id = args.get("_id")
            args.pop("_id")

        if args.get("_log"):
            logfile = os.path.abspath(args.get("_log"))
            settings.write_logfile = logfile
            args.pop("_log")
        else:
            settings.write_logfile = templog_filename()

        settings.read_logfile = settings.write_logfile
        if os.path.exists(settings.write_logfile):
            os.remove(settings.write_logfile)

        settings.output_format = args.pop("_output")

        if args.get("_database"):
            settings.database = args.pop("_database")

        if args.get("_show_skipped"):
            settings.show_skipped = True
            args.pop("_show_skipped")

        if args.get("_random_order"):
            settings.random_order = True
            args.pop("_random_order")

        if args.get("_pause_before"):
            xflags = kwargs.get("xflags", {})
            for pattern in args.get("_pause_before"):
                xflags[pattern] = xflags.get(pattern, [0, 0])
                xflags[pattern][0] |= PAUSE_BEFORE
            kwargs["xflags"] = xflags
            args.pop("_pause_before")

        if args.get("_pause_after"):
            xflags = kwargs.get("xflags", {})
            for pattern in args.get("_pause_after"):
                xflags[pattern] = xflags.get(pattern, [0, 0])
                xflags[pattern][0] |= PAUSE_AFTER
            kwargs["xflags"] = xflags
            args.pop("_pause_after")

        if args.get("_only"):
            only = []
            for pattern in args.pop("_only"):
                only.append(The(pattern))
            kwargs["only"] = only

        if args.get("_skip"):
            skip = []
            for pattern in args.pop("_skip"):
                skip.append(The(pattern))
            kwargs["skip"] = skip

        if args.get("_start"):
            pattern = args.pop("_start")[0]
            kwargs["start"] = The(pattern)

        if args.get("_end"):
            pattern = args.pop("_end")[0]
            kwargs["end"] = The(pattern)

        if args.get("_only_tags"):
            _only_tags = {}
            for item in args.pop("_only_tags"):
                _only_tags.update(item)
            kwargs["only_tags"] = TheTags(**_only_tags)

        if args.get("_skip_tags"):
            _skip_tags = {}
            for item in args.pop("_skip_tags"):
                _skip_tags.update(item)
            kwargs["skip_tags"] = TheTags(**_skip_tags)

        if args.get("_tags"):
            kwargs["tags"] = {value for value in args.pop("_tags")}

        if args.get("_attrs"):
            if kwargs.get("attributes", None) is None:
                kwargs["attributes"] = []
            kwargs["attributes"] += [Attribute(item.key, item.value) for item in args.pop("_attrs")]
            for attr in kwargs["attributes"]:
                if args.get(attr.name, None):
                    raise AttributeError(f"use test argument '--{attr.name}' instead of '--attr {attr.name}=<value>'")

        if args.get("_private_key"):
            kwargs["private_key"] = args.pop("_private_key")

        if args.get("_repeat"):
            repeat = []
            for item in args.pop("_repeat"):
                repeat.append(item)
            kwargs["repeat"] = repeat

        if args.get("_rerun"):
            rerun_individually = args.pop("_individually", False)
            rerun = args.pop("_rerun")

            if not args.get("_reference"):
                raise ExitWithError(f"--reference argument must be specified")

            results = {}
            ResultsLogPipeline(args.pop("_reference"), results, steps=False).run()

            if kwargs.get("only") is None:
                kwargs["only"] = []

            if rerun_individually is True:
                kwargs["rerun_individually"] = []

            RerunTest = namedtuple("RerunTest", "name type tags")
            rerun_tests = []
            result_types = []

            for r in rerun:
                if r == "xouts":
                    result_types += ["XOK", "XFail", "XError", "XNull"]
                elif r == "passes":
                    result_types += ["OK"]
                elif r == "fails":
                    result_types += ["Fail", "Error", "Null"]
                elif r == "ok":
                    result_types += ["OK"]
                elif r == "fail":
                    result_types += ["Fail"]
                elif r == "error":
                    result_types += ["Error"]
                elif r == "null":
                    result_types += ["Null"]
                elif r == "xfail":
                    result_types += ["XFail"]
                elif r == "xerror":
                    result_types += ["XError"]
                elif r == "xnull":
                    result_types += ["XNull"]
                elif r == "xok":
                    result_types += ["XOK"]
                elif r == "skip":
                    result_types += ["Skip"]

            for test in results["tests"].values():
                result = test["result"]
                test_type = getattr(TestType, result["test_type"])
                test_name = result["result_test"]
                test_tags = {tag["tag_value"] for tag in test["test"]["tags"]}

                if test_type >= TestType.Test:
                    if result["result_type"] in result_types:
                        found = False
                        for rerun_test in rerun_tests:
                            if rerun_test.name.startswith(test_name):
                                found = True
                                break
                        if not found:
                            rerun_tests.append(RerunTest(test_name, test_type, test_tags))

                rerun_tests.sort()
                length = len(rerun_tests)

                for i, test in enumerate(rerun_tests):
                    if i+1 < length and rerun_tests[i+1].name.startswith(test.name):
                        rerun_tests.remove(test)
                        i -= 1

            for rerun_test in rerun_tests:
                if rerun_individually is True:
                    name_parts = rerun_test.name.split(name_sep)
                    kwargs["rerun_individually"].append(RerunTest(
                        The(join(name_sep, name_parts[1], ":", *name_parts[2:], "*")),
                        rerun_test.type, rerun_test.tags))
                else:
                    kwargs["only"].append(The(join(rerun_test.name, "*")))

        if args.get("func"):
            func = args.pop("func")
            func(args, kwargs)

        if kwargs.get("private_key"):
            private_key = kwargs.get("private_key")
            for name, value in args.items():
                if isinstance(value, Secret):
                    value(public_key=private_key.pubkey)

    except (ExitException, KeyboardInterrupt, Exception) as exc:
        if not debug_processed or settings.debug:
            sys.stderr.write(warning(get_exception(), eol='\n'))
        sys.stderr.write(danger("error: " + str(exc).strip()))
        if isinstance(exc, ExitException):
            sys.exit(exc.exitcode)
        else:
            sys.exit(1)

    return args

class TestDefinition(object):
    """Test definition.

    :param name: name of the test
    :param **kwargs: test class arguments
    """
    type = TestType.Test

    def __new__(cls, name=None, **kwargs):
        run = kwargs.pop("run", None)
        test = kwargs.pop("test", None)
        no_arguments = None

        if kwargs.get("args", None):
            no_arguments = False

        if name is not None:
            kwargs["name"] = name

        def inherit_kwargs(**from_kwargs):
            _kwargs = from_kwargs
            _kwargs["args"] = dict(_kwargs["args"])
            _kwargs.update(kwargs)
            return _kwargs

        if run:
            if isinstance(run, TestDecorator):
                kwargs = inherit_kwargs(**run.func.kwargs)
                kwargs["test"] = run
            elif isinstance(run, TestDefinition):
                kwargs = inherit_kwargs(**run.kwargs, **({"name": run.name} if run.name is not None else {}))
            elif isinstance(run, TestBase) or inspect.isclass(run) and issubclass(run, (TestBase, TestDefinition)):
                kwargs["test"] = run
            else:
                raise TypeError(f"'{run}' is not a valid test type")

        elif test:
            if isinstance(test, TestDecorator):
                kwargs = inherit_kwargs(**test.func.kwargs)
                kwargs["test"] = test
            elif isinstance(test, TestDefinition):
                kwargs = inherit_kwargs(**test.kwargs, **({"name": test.name} if test.name is not None else {}))
            elif isinstance(test, TestBase) or inspect.isclass(test) and issubclass(test, (TestBase, TestDefinition)):
                kwargs["test"] = test
            else:
                raise TypeError(f"'{test}' is not a valid test type")

        self = cls.__create__(**kwargs)
        self.no_arguments = no_arguments

        if run:
            return self()
        return self

    @classmethod
    def __create__(cls,  **kwargs):
        self = super(TestDefinition, cls).__new__(cls)
        self.name = None
        self.test = None
        self.parent = None
        self.kwargs = kwargs
        self.tags = None
        self.repeat = None
        self.rerun_individually = None
        self.repeatable_func = None
        self._with_block_frame = None
        return self

    def __call__(self, *pargs, **args):
        if pargs:
            raise TypeError(f"only named arguments are allowed but {pargs} positional arguments were passed")

        test = self.kwargs.get("test", None)
        self.kwargs["args"] = dict(self.kwargs.get("args") or {})
        self.kwargs["args"].update(args)

        self.no_arguments = get(self.no_arguments, not args)

        if test and isinstance(test, TestDecorator):
            self.repeatable_func = test
            with self as _test:
                test(**self.kwargs["args"])
            return _test
        else:
            with self as _test:
                pass
            return _test

    def __enter__(self):
        _set_current_top_previous()

        def dummy(*args, **kwargs):
            pass
        try:
            kwargs = self.kwargs
            kwargs["args"] = dict(kwargs.get("args") or {})

            argparser = kwargs.pop("argparser", None)
            parent = kwargs.pop("parent", None) or current()
            keep_type = kwargs.pop("keep_type", None)
            format_name = kwargs.pop("format_name", False)
            format_description = kwargs.pop("format_description", False)

            if not top():
                cli_args = parse_cli_args(self.kwargs, cli_argparser(self.kwargs, argparser if not isinstance(argparser, ArgumentParser) else argparser.value))
                kwargs["args"].update({k: v for k,v in cli_args.items() if not k.startswith("_")})

            test = kwargs.pop("test", None)
            kwargs_test = test
            if test and isinstance(test, TestDecorator):
                test = test.func.kwargs.get("test", None)
            test = test if test is not None else TestBase
            if not issubclass(test, TestBase):
                raise TypeError(f"{test} must be subclass of TestBase")

            name = test.make_name(kwargs.pop("name", None), parent.name if parent else None, kwargs["args"], format=format_name)
            kwargs["flags"] = Flags(kwargs.get("flags"))

            if parent:
                kwargs["parent"] = parent
                with parent.lock:
                    kwargs["id"] = parent.id + [parent.child_count]
                    parent.child_count += 1
                kwargs["cflags"] = parent.cflags
                # propagate manual flag if automatic test flag is not set
                if not kwargs["flags"] & AUTO:
                    kwargs["flags"] |= parent.flags & MANUAL
                # propagate xfails, xflags that prefix match the name of the test
                kwargs["xfails"] = {
                    k: v for k, v in parent.xfails.items() if match(name, k, prefix=True)
                } if parent.xfails else None or kwargs.get("xfails")
                kwargs["xflags"] = {
                    k: v for k, v in parent.xflags.items() if match(name, k, prefix=True)
                } if parent.xflags else None or kwargs.get("xflags")
                # propagate only, skip, start, and end
                kwargs["only"] = parent.only or kwargs.get("only")
                kwargs["skip"] = parent.skip or kwargs.get("skip")
                kwargs["start"] = parent.start or kwargs.get("start")
                kwargs["end"] = parent.end or kwargs.get("end")
                kwargs["only_tags"] = parent.only_tags or kwargs.get("only_tags")
                kwargs["skip_tags"] = parent.skip_tags or kwargs.get("skip_tags")
                # propagate repeat
                if parent.repeat and parent.type > TestType.Outline and self.type >= TestType.Outline:
                    kwargs["repeat"] = parent.repeat
                # handle parent test type propagation
                if keep_type is None:
                    self._parent_type_propagation(parent, kwargs)

            self.name = name
            self.tags = test.make_tags(kwargs.pop("tags", None))
            self.description = test.make_description(kwargs.pop("description", None), kwargs["args"], format=format_description)
            self.parent = parent

            # anchor all patterns
            kwargs["xfails"] = {
                absname(k, name if name else name_sep): v for k, v in dict(kwargs.get("xfails") or {}).items()
            } or None
            kwargs["xflags"] = {
                absname(k, name if name else name_sep): v for k, v in dict(kwargs.get("xflags") or {}).items()
            } or None
            kwargs["only"] = [The(str(f)).at(name if name else name_sep) for f in kwargs.get("only") or []] or None
            kwargs["skip"] = [The(str(f)).at(name if name else name_sep) for f in kwargs.get("skip") or []] or None
            kwargs["start"] = The(str(kwargs.get("start"))).at(name if name else name_sep) if kwargs.get("start") else None
            kwargs["end"] = The(str(kwargs.get("end"))).at(name if name else name_sep) if kwargs.get("end") else None
            if not isinstance(kwargs.get("only_tags"), TheTags):
                kwargs["only_tags"] = TheTags(**dict(kwargs["only_tags"])) if kwargs.get("only_tags") else None
            else:
                kwargs["only_tags"] = kwargs.get("only_tags")
            if not isinstance(kwargs.get("skip_tags"), TheTags):
                kwargs["skip_tags"] = TheTags(**dict(kwargs["skip_tags"])) if kwargs.get("skip_tags") else None
            else:
                kwargs["skip_tags"] = kwargs.get("skip_tags")
            kwargs["repeat"] = [RepeatTest(*r) for r in kwargs.get("repeat", [])] or None
            if kwargs["repeat"]:
                [r.pattern.at(name if name else name_sep) for r in kwargs["repeat"]]

            self._apply_xflags(name, kwargs)
            self._apply_start(name, parent, kwargs)
            self._apply_only_tags(self.type, self.tags, kwargs)
            self._apply_skip_tags(self.type, self.tags, kwargs)
            self._apply_skip(name, kwargs)
            self._apply_end(name, parent, kwargs)
            self._apply_only(name, kwargs)

            # for And subtype we change the subtype to be that of its sibling
            if kwargs.get("subtype") is TestSubType.And:
                sibling = None
                prev = previous()
                if prev and depth(prev.name) == depth(name):
                    sibling = prev
                if not sibling:
                    raise TypeError("`And` subtype can't be used here as it has no sibling from which to inherit the subtype")
                if sibling.type != kwargs["type"]:
                    raise TypeError("`And` subtype can't be used here as it sibling is not of the same type")
                kwargs["subtype"] = sibling.subtype

            # should not skip Background, Given and Finally steps
            if kwargs.get("subtype") in (TestSubType.Background, TestSubType.Given, TestSubType.Finally) or kwargs["flags"] & MANDATORY:
                kwargs["flags"] &= ~SKIP
                kwargs["only"] = None
                kwargs["skip"] = None
                kwargs["start"] = None
                kwargs["end"] = None
                kwargs["only_tags"] = None
                kwargs["skip_tags"] = None

            if not top():
                # can't skip, pause before or after top level test
                kwargs["flags"] &= ~SKIP
                kwargs["flags"] &= ~PAUSE_BEFORE
                kwargs["flags"] &= ~PAUSE_AFTER

            self.repeat = kwargs.pop("repeat", None)
            self.rerun_individually = kwargs.pop("rerun_individually", None)

            if self.rerun_individually:
                def transform_pattern(pattern):
                    if isabs(pattern):
                        parts = pattern.split(name_sep)
                        return join(name_sep, parts[1], ":", *parts[2:])
                    return pattern

                # need to fix all anchored patterns
                kwargs["xfails"] = {transform_pattern(k): v for k, v in
                    (kwargs.pop("xfails", {}) or {}).items()} or None
                kwargs["xflags"] = {transform_pattern(k): v for k, v in
                    (kwargs.pop("xflags", {}) or {}).items()} or None
                kwargs["only"] = [The(transform_pattern(str(f))) for f in kwargs.get("only") or []] or None
                kwargs["skip"] = [The(transform_pattern(str(f))) for f in kwargs.get("skip") or []] or None
                kwargs["start"] = The(transform_pattern(str(kwargs.get("start")))) if kwargs.get("start") else None
                kwargs["end"] = The(transform_pattern(str(kwargs.get("end")))) if kwargs.get("end") else None
                for r in self.repeat or []:
                    r.pattern.set(transform_pattern(str(r.pattern)))

            self.test = test(name, tags=self.tags, description=self.description, repeat=self.repeat, **kwargs)
            if getattr(self, "parent_type", None):
                self.test.parent_type = self.parent_type

            # indicate that parent is running an outline
            # and if there are any user arguments for an outline
            if isinstance(kwargs_test, TestOutline):
                self.test._run_outline_with_no_arguments = self.no_arguments
                self.test._run_outline = True

            if self.rerun_individually is not None:
                self.trace = sys.gettrace()
                sys.settrace(dummy)
                sys._getframe(1).f_trace = functools.partial(self.__rerun_individually__, self.rerun_individually, None, None, None)
                return

            if self.repeat is not None:
                repeat = self._apply_repeat(name, self.repeat)
                if repeat is not None:
                    self.trace = sys.gettrace()
                    sys.settrace(dummy)
                    sys._getframe(1).f_trace = functools.partial(self.__repeat__, repeat, None, None, None)
                    return

        except (KeyboardInterrupt, Exception):
            raise

        try:
            return self.test._enter()
        except (KeyboardInterrupt, Exception) as exc:
            if not self.test.io:
                raise

            frame = inspect.currentframe().f_back
            self._with_block_frame = (frame, frame.f_lasti, frame.f_lineno)
            self.trace = sys.gettrace()
            sys.settrace(dummy)
            sys._getframe(1).f_trace = functools.partial(self.__nop__, *sys.exc_info())

    def _apply_end(self, name, parent, kwargs):
        end = kwargs.get("end")
        if not end:
            return

        if end.match(name):
            if parent:
                with parent.lock:
                    parent.end = None
                    parent.skip = [The("/*")]

    def _apply_start(self, name, parent, kwargs):
        start = kwargs.get("start")
        if not start:
            return

        if not start.match(name):
            kwargs["flags"] |= SKIP
        elif start.match(name, prefix=False):
            kwargs["start"] = None
            if parent:
                with parent.lock:
                    parent.start = None

    def _apply_repeat(self, name, repeat):
        if not repeat:
            return

        for item in repeat:
            if item.pattern.match(name, prefix=False):
                return item

    def _apply_only_tags(self, type, tags, kwargs):
        only_tags = (kwargs.get("only_tags", {}) or {}).get(type)
        if not only_tags:
            return

        found = len({tag for tag in only_tags if tag in tags}) > 0
        if not found:
            kwargs["flags"] |= SKIP

    def _apply_skip_tags(self, type, tags, kwargs):
        skip_tags = (kwargs.get("skip_tags", {}) or {}).get(type)
        if not skip_tags:
            return

        found = len({tag for tag in skip_tags if tag in tags}) > 0
        if found:
            kwargs["flags"] |= SKIP

    def _apply_only(self, name, kwargs):
        only = kwargs.get("only")
        if not only:
            return

        found = False
        for item in only:
            if item.match(name):
                found = True
                break

        if not found:
            kwargs["flags"] |= SKIP

    def _apply_skip(self, name, kwargs):
        skip = kwargs.get("skip")
        if not skip:
            return

        for item in skip:
            if item.match(name, prefix=False):
                kwargs["flags"] |= SKIP
                break

    def _apply_xflags(self, name, kwargs):
        xflags = kwargs.get("xflags")
        if not xflags:
            return

        for pattern, item in xflags.items():
            if match(name, pattern):
                set_flags, clear_flags = item
                kwargs["flags"] = (kwargs["flags"] & ~Flags(clear_flags)) | Flags(set_flags)

    def _parent_type_propagation(self, parent, kwargs):
        """Propagate parent test type if lower.

        :param parent: parent
        :param kwargs: test's kwargs
        """
        type = kwargs.pop("type", TestType.Test)
        subtype = kwargs.pop("subtype", None)

        parent_type = parent.type

        if parent_type == TestType.Iteration:
            parent_type = parent.parent_type

        if int(parent_type) < int(type):
            type = parent.type
            subtype = parent.subtype

        elif subtype is TestSubType.Example:
            type = parent_type

        kwargs["subtype"] = subtype
        kwargs["type"] = type

    def __repeat__(self, repeat=None, *args):
        sys.settrace(self.trace)
        raise TestIteration(repeat)

    def __rerun_individually__(self, patterns, *args):
        sys.settrace(self.trace)
        raise TestRerunIndividually(patterns)

    def __nop__(self, exc_type, exc_value, exc_tb, *args):
        sys.settrace(self.trace)
        raise exc_value.with_traceback(exc_tb)

    def __exit__(self, exception_type, exception_value, exception_traceback):
        frame = inspect.currentframe().f_back
        co_filename_filter = "testflows/_core"

        def make_complete_traceback(exception_traceback, frame):
            tb = namedtuple('tb', ('tb_frame', 'tb_lasti', 'tb_lineno', 'tb_next'))

            def walk_frame(frame, tb_next=None):
                if frame is None:
                    return tb_next
                if not settings.debug and co_filename_filter in frame.f_code.co_filename:
                    tb_next = tb_next
                else:
                    tb_next = tb(frame, frame.f_lasti, frame.f_lineno, tb_next)
                return walk_frame(frame.f_back, tb_next)

            def walk_tb(tb_frame):
                tb_next = None
                if tb_frame.tb_next:
                    tb_next = walk_tb(tb_frame.tb_next)

                if tb_frame and not settings.debug and co_filename_filter in tb_frame.tb_frame.f_code.co_filename:
                    return tb_next
                else:
                    return tb(tb_frame.tb_frame, tb_frame.tb_lasti, tb_frame.tb_lineno, tb_next)

            tb_next = walk_tb(exception_traceback)
            if self._with_block_frame is not None:
                # if self._with_block_frame is set it means an exception was raised
                # in __enter__() during test._enter() call. Now we need to fix
                # traceback so that includes the line where "with" block is defined
                # as it is lost
                _frame, _lasti, _lineno = self._with_block_frame
                if tb_next:
                    tb_next = tb_next.tb_next
                if tb_next:
                    tb_next = tb_next.tb_next
                tb_next = tb(_frame, _lasti, _lineno, tb_next)
            tb_start = walk_frame(frame.f_back, tb_next)
            return tb_start

        if exception_value:
            exception_traceback = make_complete_traceback(exception_traceback, frame)

        if isinstance(exception_value, TestIteration):
            try:
                repeat = exception_value.repeat

                self.test._enter()
                if self.repeatable_func is None:
                    raise Error("not repeatable")

                __kwargs = dict(self.kwargs)
                __kwargs.pop("name", None)
                __kwargs.pop("parent", None)
                __kwargs["type"] = TestType.Iteration
                __args = __kwargs.pop("args", {})

                if repeat.until == "fail":
                    __kwargs["flags"] = Flags(__kwargs.get("flags")) & ~TE
                else:
                    # pass or complete
                    __kwargs["flags"] = Flags(__kwargs.get("flags")) | TE

                for i in range(repeat.number):
                    with Iteration(name=f"{i}", tags=self.tags, **__kwargs, parent_type=self.test.type) as iteration:
                        if isinstance(self.repeatable_func, TestOutline):
                            iteration._run_outline_with_no_arguments = self.no_arguments
                            iteration._run_outline = True
                        self.repeatable_func(**__args)
                    if repeat.until == "pass" and isinstance(iteration.result, PassResults):
                        break
            except:
                try:
                    test__exit__ = self.test._exit(*sys.exc_info())
                except(KeyboardInterrupt, Exception):
                    raise
            else:
                try:
                    test__exit__ = self.test._exit(None, None, None)
                except(KeyboardInterrupt, Exception):
                    raise

        elif isinstance(exception_value, TestRerunIndividually):
            try:
                rerun_tests = exception_value.tests

                self.test._enter()

                if self.repeatable_func is None:
                    raise Error("not repeatable")

                for i, rerun_test in enumerate(rerun_tests):
                    __kwargs = dict(self.kwargs)
                    __kwargs.pop("name", None)
                    __kwargs.pop("parent", None)
                    __kwargs["flags"] = Flags(__kwargs.get("flags")) | TE
                    __kwargs["type"] = TestType.Iteration
                    __args = __kwargs.pop("args", {})

                    rerun_name = rerun_test.name.pattern.rstrip(name_sep + "*")

                    self._apply_start(rerun_name, self.parent, __kwargs)
                    self._apply_only_tags(rerun_test.type, rerun_test.tags, __kwargs)
                    self._apply_skip_tags(rerun_test.type, rerun_test.tags, __kwargs)
                    self._apply_skip(rerun_name, __kwargs)
                    self._apply_end(rerun_name, self.parent, __kwargs)
                    self._apply_only(rerun_name, __kwargs)

                    __only = [rerun_test.name] + (__kwargs.pop("only", []) or [])

                    with Module(name=f"{i}", only=__only, tags=self.tags, **__kwargs) as iteration:
                        if isinstance(self.repeatable_func, TestOutline):
                            iteration._run_outline_with_no_arguments = self.no_arguments
                            iteration._run_outline = True
                        self.repeatable_func(**__args)
            except:
                try:
                    test__exit__ = self.test._exit(*sys.exc_info())
                except(KeyboardInterrupt, Exception):
                    raise
            else:
                try:
                    test__exit__ = self.test._exit(None, None, None)
                except(KeyboardInterrupt, Exception):
                    raise
        else:
            try:
                test__exit__ = self.test._exit(exception_type, exception_value, exception_traceback)
            except (KeyboardInterrupt, Exception):
                raise

        if not self.parent:
            if not test__exit__:
                sys.stderr.write(warning(get_exception(exception_type, exception_value, exception_traceback), eol='\n'))
                sys.stderr.write(danger("error: " + str(exception_value).strip()))
                sys.exit(1)
            sys.exit(0 if self.test.result else 1)

        if isinstance(exception_value, KeyboardInterrupt):
            raise KeyboardInterrupt

        # if test did not handle the exception in _exit then re-raise it
        if exception_value and not test__exit__:
            raise exception_value

        if not self.test.result:
            if isinstance(self.test.result, Fail):
                result = Fail(test=self.parent.name, message=self.test.result.message)
            else:
                # convert Null into an Error
                result = Error(test=self.parent.name, message=self.test.result.message)

            if TE not in self.test.flags:
                raise result
            else:
                with self.parent.lock:
                    if isinstance(self.parent.result, Error):
                        pass
                    elif isinstance(self.test.result, Error) and ERROR_NOT_COUNTED not in self.test.flags:
                        self.parent.result = result
                    elif isinstance(self.test.result, Null) and NULL_NOT_COUNTED not in self.test.flags:
                        self.parent.result = result
                    elif isinstance(self.parent.result, Fail):
                        pass
                    elif isinstance(self.test.result, Fail) and FAIL_NOT_COUNTED not in self.test.flags:
                        self.parent.result = result
                    else:
                        pass
        return True

class Module(TestDefinition):
    """Module definition."""
    type = TestType.Module

    def __new__(cls, name=None, **kwargs):
        kwargs["type"] = TestType.Module
        return super(Module, cls).__new__(cls, name, **kwargs)

class Suite(TestDefinition):
    """Suite definition."""
    type = TestType.Suite

    def __new__(cls, name=None, **kwargs):
        kwargs["type"] = TestType.Suite
        return super(Suite, cls).__new__(cls, name, **kwargs)

class Outline(TestDefinition):
    """Outline definition."""
    type = TestType.Outline

    def __new__(cls, name=None, **kwargs):
        kwargs["type"] = kwargs.pop("type", cls.type)
        return super(Outline, cls).__new__(cls, name, **kwargs)

class Test(TestDefinition):
    """Test definition."""
    type = TestType.Test

    def __new__(cls, name=None, **kwargs):
        kwargs["type"] = TestType.Test
        return super(Test, cls).__new__(cls, name, **kwargs)

class Iteration(TestDefinition):
    """Test iteration definition."""
    type = TestType.Iteration

    def __new__(cls, name=None, **kwargs):
        kwargs["type"] = TestType.Iteration
        parent_type = kwargs.pop("parent_type", TestType.Test)
        self = super(Iteration, cls).__new__(cls, name, **kwargs)
        self.parent_type = parent_type
        return self

class Example(TestDefinition):
    """Example definition."""
    def __new__(cls, name=None, **kwargs):
        kwargs["type"] = kwargs.pop("type", cls.type)
        kwargs["subtype"] = TestSubType.Example
        self = super(Example, cls).__new__(cls, name, **kwargs)
        return self

class Step(TestDefinition):
    """Step definition."""
    type = TestType.Step
    subtype = None

    def __new__(cls, name=None, **kwargs):
        kwargs["type"] = kwargs.pop("type", cls.type)
        kwargs["subtype"] = kwargs.pop("subtype", cls.subtype)
        return super(Step, cls).__new__(cls, name, **kwargs)

# support for BDD
class Feature(Suite):
    def __new__(cls, name=None, **kwargs):
        kwargs["subtype"] = TestSubType.Feature
        return super(Feature, cls).__new__(cls, name, **kwargs)

class Scenario(Test):
    def __new__(cls, name=None, **kwargs):
        kwargs["subtype"] = TestSubType.Scenario
        return super(Scenario, cls).__new__(cls, name, **kwargs)

class Check(Test):
    def __new__(cls, name=None, **kwargs):
        kwargs["subtype"] = TestSubType.Check
        return super(Check, cls).__new__(cls, name, **kwargs)

class BackgroundTest(TestBase):
    def __init__(self, *args, **kwargs):
        self.contexts = []
        super(BackgroundTest, self).__init__(*args, **kwargs)

    def _enter(self):
        self.stack = ExitStack().__enter__()
        self.context.cleanup(self.stack.__exit__, None, None, None)
        return super(BackgroundTest, self)._enter()

    def append(self, ctx_manager):
        ctx = self.stack.enter_context(ctx_manager)
        self.contexts.append(ctx)
        return ctx

    def __iter__(self):
        return iter(self.contexts)

class Background(Step):
    subtype = TestSubType.Background

    def __new__(cls, name=None, **kwargs):
        kwargs["test"] = kwargs.pop("test", BackgroundTest)
        return super(Background, cls).__new__(cls, name, **kwargs)

class Given(Step):
    subtype = TestSubType.Given

class When(Step):
    subtype = TestSubType.When

class Then(Step):
    subtype = TestSubType.Then

class And(Step):
    subtype = TestSubType.And

class But(Step):
    subtype = TestSubType.But

class By(Step):
    subtype = TestSubType.By

class Finally(Step):
    subtype = TestSubType.Finally

class NullStep():
    def __enter__(self):
        return None

    def __exit__(self, *args, **kwargs):
        return False

# decorators
class TestDecorator(object):
    type = Test

    def __init__(self, func):
        self.func = func

        self.func.type = self.type.type
        self.func.name = getattr(self.func, "name", self.func.__name__.replace("_", " "))
        self.func.description = getattr(self.func, "description", self.func.__doc__)

        signature = inspect.signature(self.func)

        args = getattr(self.func, "args", {})
        default_args = {p.name: p.default for p in signature.parameters.values() if
            p.default != inspect.Parameter.empty}

        self.func.args = default_args
        self.func.args.update(args)

        kwargs = dict(vars(self.func))

        self.func.kwargs = kwargs

        _type = self.type
        functools.update_wrapper(self, self.func)
        self.type = _type

    def __call__(self, *pargs, **args):
        if pargs:
            raise TypeError(f"only named arguments are allowed but {pargs} positional arguments were passed")

        return self.__run__(**args)

    def __run__(self, **args):
        _set_current_top_previous()

        test = current()

        def process_func_result(r):
            if inspect.isgenerator(r):
                res = run_generator(r)
                test.context.cleanup(run_generator, r)
                r = res

            return r

        def run(test):
            return process_func_result(self.func(test, **args))

        test_running_outline = getattr(test, "_run_outline", False)

        if (test is None
                or (test and test.type > self.type.type and self.type.type != TestType.Outline)
                or (test and test_running_outline)):
            kwargs = dict(self.func.kwargs)

            if isinstance(self, TestOutline):
                no_arguments = not args or getattr(test, "_run_outline_with_no_arguments", False)
                examples = test_running_outline and getattr(test, "examples") or self.examples

                if no_arguments and examples:
                    kwargs["args"] = {}
                    kwargs.pop("test", None)

                    _test_type = self.type(**kwargs, test=self)

                    def execute_examples():
                        for example in examples:
                            _kwargs = dict(self.func.kwargs)
                            _kwargs["name"] = str(example)
                            _kwargs["args"] = dict(kwargs.get("args", {}))
                            _kwargs["args"].update(vars(example))
                            _kwargs.update(dict(examples.args))
                            _kwargs.update(dict(example._args))
                            _kwargs.pop("type", None)
                            _kwargs.pop("examples", None)

                            if _test.type == TestType.Iteration:
                                type = _test.parent_type
                            else:
                                type = _test.type

                            _example_type = Example(type=type, **_kwargs)

                            def execute_example(**args):
                                process_func_result(self.func(current(), **args))

                            _example_type.repeatable_func = execute_example

                            with _example_type as _example:
                                execute_example(**vars(example))

                    _test_type.repeatable_func = execute_examples

                    if test and test_running_outline:
                        _test = test
                        execute_examples()
                    else:
                        with _test_type as _test:
                            execute_examples()

                    return _test
                else:
                    if test and test_running_outline:
                        return run(test)
                    else:
                        kwargs.pop("test", None)
                        return self.type(**kwargs, test=self)(**args)
            else:
                kwargs.pop("test", None)
                return self.type(**kwargs, test=self)(**args)
        else:
            return run(test)

class TestStep(TestDecorator):
    type = Step
    subtype = None

    def __init__(self, func_or_subtype=None):
        self.func = None

        if inspect.isfunction(func_or_subtype):
            self.func = func_or_subtype
        elif func_or_subtype is not None:
            self.subtype = func_or_subtype.subtype

        if self.func:
            TestDecorator.__init__(self, self.func)

    def __call__(self, *args, **kwargs):
        if not self.func:
            self.func = args[0]
            if self.subtype is not None:
                self.func.subtype = self.subtype
            TestDecorator.__init__(self, self.func)
            return self

        return super(TestStep, self).__call__(*args, **kwargs)

class TestOutline(TestDecorator):
    type = Outline

    def __init__(self, func_or_type=None):
        self.func = None
        self.examples = None

        if inspect.isfunction(func_or_type):
            self.func = func_or_type
        elif func_or_type is not None:
            self.type = func_or_type

        if self.func:
            self._init_func()
            TestDecorator.__init__(self, self.func)

    def _init_func(self):
        if getattr(self.func, "examples", None):
            self.examples = self.func.examples

    def __call__(self, *args, **kwargs):
        if not self.func:
            self.func = args[0]
            self._init_func()
            TestDecorator.__init__(self, self.func)
            return self

        return super(TestOutline, self).__call__(*args, **kwargs)

class TestCase(TestDecorator):
    type = Test

class TestScenario(TestCase):
    type = Scenario

class TestCheck(TestCase):
    type = Check

class TestSuite(TestDecorator):
    type = Suite

class TestFeature(TestSuite):
    type = Feature

class TestModule(TestDecorator):
    type = Module

class TestBackground(TestDecorator):
    type = Background

    def __init__(self, func):
        func.test = getattr(func, "test", BackgroundTest)
        if not issubclass(func.test, BackgroundTest):
            raise TypeError(f"{func.test} not a subclass of BackgroundTest")
        return super(TestBackground, self).__init__(func)

def ordered(tests):
    """Return ordered list of tests.
    """
    if settings.random_order:
        random.shuffle(tests)
    else:
        human_sort(tests, key=lambda test: test.__name__)
    return tests

def loads(name, *types, package=None, frame=None, filter=None):
    """Load multiple tests from module.

    :param name: module name or module
    :param *types: test types (Step, Test, Scenario, Suite, Feature, or Module), default: all
    :param package: package name if module name is relative (optional)
    :param frame: caller frame if module name is not specified (optional)
    :param filter: filter function
    :return: list of tests
    """
    if name is None or name == ".":
        if frame is None:
            frame = inspect.currentframe().f_back
        module = sys.modules[frame.f_globals["__name__"]]
    elif inspect.ismodule(name):
        module = name
    else:
        module = importlib.import_module(name, package=package)

    def is_type(member):
        if isinstance(member, TestDecorator):
            if not types:
                return True
            return member.type in types

    tests = ordered([test for name, test in inspect.getmembers(module, is_type)])
    
    if filter:
        return builtins.filter(filter, tests)
    
    return tests
