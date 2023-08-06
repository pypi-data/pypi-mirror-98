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
import inspect
import importlib
import threading
import builtins
import functools

from .message import Message, dumps
from .name import basename
from .objects import OK, Fail, Error, Skip, Null
from .objects import XOK, XFail, XError, XNull
from .objects import Value, Metric, Ticket, Attribute, Tag, Requirement, Node

#: thread local values
_current_test = {}
_current_test_lock = threading.Lock()

def _set_current_top_previous():
    """Set current, top and previous
    using the parent thread if needed.
    """
    current_thread = threading.current_thread()

    if getattr(current_thread, "_parent", None):
        if current() is not None:
            return

        parent_current = current(thread=current_thread._parent)

        if parent_current is not None:
            parent_top = top(thread=current_thread._parent)
            parent_previous = previous(thread=current_thread._parent)
            current(value=parent_current)
            top(value=parent_top)
            previous(value=parent_previous)

def top(value=None, thread=None):
    """Highest level test.
    """
    with _current_test_lock:
        if thread is None:
            thread = threading.current_thread()
        if _current_test.get(thread.name) is None:
            _current_test[thread.name] = {}
        if value is not None:
            _current_test[thread.name]["main"] = value
        return _current_test[thread.name].get("main")

def current(value=None, thread=None, set_value=False):
    """Currently executing test.
    """
    with _current_test_lock:
        if thread is None:
            thread = threading.current_thread()
        if _current_test.get(thread.name) is None:
            _current_test[thread.name] = {}
        if value is not None or set_value:
            _current_test[thread.name]["object"] = value
        return _current_test[thread.name].get("object")

def previous(value=None, thread=None):
    """Last executed test.
    """
    with _current_test_lock:
        if thread is None:
            thread = threading.current_thread()
        if _current_test.get(thread.name) is None:
            _current_test[thread.name] = {}
        if value is not None:
            _current_test[thread.name]["previous"] = value
        return _current_test[thread.name].get("previous")

def current_dir(frame=None):
    """Return directory of the current source file.
    """
    if frame is None:
        frame = inspect.currentframe().f_back
    return os.path.dirname(os.path.abspath(frame.f_globals["__file__"]))

def current_module(frame=None):
    """Return reference to the current module.
    """
    if frame is None:
        frame = inspect.currentframe().f_back
    return sys.modules[frame.f_globals["__name__"]]

def load_module(name, package=None):
    """Load module by name.
    """
    return importlib.import_module(module, package=package)

def load(name, test=None, package=None, frame=None):
    """Load test by name from module.

    :param name: module name or module
    :param test: test class or method name to load (optional)
    :param package: package if module name is relative (optional)
    """
    if name is None or name == ".":
        if frame is None:
            frame = inspect.currentframe().f_back
        module = sys.modules[frame.f_globals["__name__"]]
    elif inspect.ismodule(name):
        module = name
    else:
        module = importlib.import_module(name, package=package)
    if test:
        test = getattr(module, test, None)
    if test is None:
        test = getattr(module, "TestCase", None)
    if test is None:
        test = getattr(module, "TestSuite", None)
    if test is None:
        test = getattr(module, "Test", None)
    return test

def append_path(pathlist, path, *rest, **kwargs):
    """Append path relative to the caller
    to the path list.

    :param pathlist: path list
    :param path: path relative to the caller
    :param *rest: rest of the path
    :param pos: insert at given position,
       default: append to the end of the list
    """
    pos = kwargs.pop("pos", None)
    frame = inspect.currentframe().f_back
    dir = os.path.join(os.path.dirname(os.path.abspath(frame.f_globals["__file__"])), path, *rest)
    if dir not in pathlist:
        if pos is None:
            pathlist.append(dir)
        else:
            pathlist.insert(pos, dir)
    return pathlist

def main(frame=None):
    """Return true if caller is the main module.

    :param frame: caller frame
    """
    if frame is None:
        frame = inspect.currentframe().f_back
    return frame.f_globals["__name__"] == "__main__"

class args(dict):
    pass

def attribute(name, value, type=None, group=None, uid=None, base=Attribute, test=None):
    obj = base(name=name, value=value, type=type, group=group, uid=uid)
    if test is None:
        test = current()
    if test.attributes.get(obj.name, None) is not None:
        raise NameError(f"attribute named '{obj.name}' already exists")
    test.attributes[obj.name] = obj
    test.io.output.attribute(obj)

def requirement(name, version, description=None, link=None,
        priority=None, type=None, group=None, uid=None, base=Requirement, test=None):
    obj = base(name=name, version=version, description=description, link=link,
        priority=priority, type=type, group=group, uid=uid)
    if test is None:
        test = current()
    if test.requirements.get(obj.name, None) is not None:
        raise NameError(f"requirement named '{obj.name}' already exists")
    test.requirements[obj.name] = obj
    test.io.output.requirement(obj)

def tag(value, test=None):
    value = str(value)
    if test is None:
        test = current()
    test.tags.add(value)
    test.io.output.tag(Tag(value))

def metric(name, value, units, type=None, group=None, uid=None, base=Metric, test=None):
    obj = base(name=name, value=value, units=units, type=type, group=group, uid=uid)
    if test is None:
        test = current()
    test.result.metrics.append(obj)
    test.io.output.metric(obj)

def ticket(name, link=None, type=None, group=None, uid=None, base=Ticket, test=None):
    obj = base(name=name, link=link, type=type, group=group, uid=uid)
    if test is None:
        test = current()
    test.result.tickets.append(obj)
    test.io.output.ticket(obj)

def value(name, value, type=None, group=None, uid=None, base=Value, test=None):
    obj = base(name=name, value=value, type=type, group=group, uid=uid)
    if test is None:
        test = current()
    test.result.values.append(obj)
    test.io.output.value(obj)
    return value

def private_key(value=None, test=None):
    if test is None:
        test = current()
    if value is not None:
        test.private_key = value
    else:
        value = test.private_key
    return value

def note(message, test=None):
    if test is None:
        test = current()
    test.io.output.note(message)

def debug(message, test=None):
    if test is None:
        test = current()
    test.io.output.debug(message)

def trace(message, test=None):
    if test is None:
        test = current()
    test.io.output.trace(message)

def message(message, test=None):
    if test is None:
        test = current()
    test.io.output.message(Message.NONE, {"message": str(message)})

def exception(exc_type=None, exc_value=None, exc_traceback=None, test=None):
    if test is None:
        test = current()
    test.io.output.exception(exc_type, exc_value, exc_traceback)

def result(type, *args, test=None):
    if type is OK:
        return ok(*args, test=test)
    elif type is Fail:
        return fail(*args, test=test)
    elif type is Skip:
        return skip(*args, test=test)
    elif type is Error:
        return err(*args, test=test)
    elif type is Null:
        return null(*args, test=test)
    elif type is XOK:
        return xok(*args, test=test)
    elif type is XFail:
        return xfail(*args, test=test)
    elif type is XNull:
        return xnull(*args, test=test)
    raise TypeError(f"invalid result type {type}")

def ok(message=None, test=None):
    if test is None:
        test = current()
    test.result = OK(test=test.name, message=message)
    raise test.result

def fail(message=None, test=None):
    if test is None:
        test = current()
    test.result = Fail(test=test.name, message=message)
    raise test.result

def skip(message=None, test=None):
    if test is None:
        test = current()
    test.result = Skip(test=test.name, message=message)
    raise test.result

def err(message=None, test=None):
    if test is None:
        test = current()
    test.result = Error(test=test.name, message=message)
    raise test.result

def null(message=None, test=None):
    if test is None:
        test = current()
    test.result = Null(test=test.name, message=message)
    raise test.result

def xok(message=None, reason=None, test=None):
    if test is None:
        test = current()
    test.result = XOK(test=test.name, message=message, reason=reason)
    raise test.result

def xfail(message=None, reason=None, test=None):
    if test is None:
        test = current()
    test.result = XFail(test=test.name, message=message, reason=reason)
    raise test.result

def xerr(message=None, reason=None, test=None):
    if test is None:
        test = current()
    test.result = XError(test=test.name, message=message, reason=reason)
    raise test.result

def xnull(message=None, reason=None, test=None):
    if test is None:
        test = current()
    test.result = XNull(test=test.name, message=message, reason=reason)
    raise test.result

def pause(test=None):
    if test is None:
        test = current()
    test.io.output.prompt("Paused, enter any key to continue...")
    builtins.input()
    test.io.output.input("")

def input(type, multiline=False, choices=None, confirm=True, test=None):
    nl = "\n"

    if test is None:
        test = current()

    def confirmed():
        prompt = "Is this correct [Y/n]? "
        test.io.output.prompt(prompt)
        answer = builtins.input()
        test.io.output.input(answer or "Y")
        return answer in ["Y", "y", ""]

    def multilined():
        lines = []
        while True:
            try:
                lines.append(builtins.input())
            except EOFError:
                break
        return '\n'.join(lines)

    if builtins.type(type) is str:
        while True:
            test.io.output.prompt(f"{type.strip()}{(nl + '(Press Enter then Ctrl-D to finish)') if multiline else ''}\n\n"
                f"{('[' + ','.join([repr(c) for c in choices]) + ']' + nl*2) if choices else ''}")
            if multiline:
                text = multilined()
            else:
                text = builtins.input()

            test.io.output.input(text)

            if choices:
                if text not in choices:
                    continue

            if confirm:
                if confirmed():
                    break
            else:
                break

        return text

    elif type is result:
        input_results_map = {
            "ok": ok,
            "": ok,
            "fail": fail,
            "error": err,
            "null": null,
            "skip": skip,
            "xfail": functools.partial(xfail, None),
            "xerror": functools.partial(xerr, None),
            "xok": functools.partial(xok, None),
            "xnull": functools.partial(xnull, None),
        }

        while True:
            test.io.output.prompt(f"Enter `{basename(test.name)}` result? ")
            input_result = builtins.input()
            test.io.output.input(input_result or "OK")

            if input_results_map.get(input_result.split(" ", 1)[0].lower()) is None:
                continue

            if confirm:
                if confirmed():
                    break
            else:
                break

        message_or_reason = None

        if " " in input_result:
            message_or_reason = input_result.split(" ", 1)[-1]

        input_results_map.get(input_result.split(" ", 1)[0].lower())(message_or_reason)

    else:
        raise ValueError(f"invalid type {type}")

def getsattr(obj, name, *default):
    """Get attribute or set it to the default value.
    """
    value = getattr(obj, name, *default)
    setattr(obj, name, value)
    return value
