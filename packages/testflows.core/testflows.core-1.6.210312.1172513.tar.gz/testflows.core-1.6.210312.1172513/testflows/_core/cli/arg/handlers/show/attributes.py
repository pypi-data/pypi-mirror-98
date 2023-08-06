# Copyright 2021 Katteli Inc.
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
import threading
import testflows._core.cli.arg.type as argtype

from testflows._core.cli.arg.common import epilog
from testflows._core.cli.arg.common import HelpFormatter
from testflows._core.cli.arg.handlers.handler import Handler as HandlerBase
from testflows._core.message import Message
from testflows._core.transform.log.pipeline import Pipeline as PipelineBase
from testflows._core.transform.log.read_and_filter import transform as read_and_filter_transform
from testflows._core.transform.log.flat import transform as flat_transform
from testflows._core.transform.log.parse import transform as parse_transform
from testflows._core.transform.log.sort import transform as sort_transform
from testflows._core.transform.log.write import transform as write_transform

class Handler(HandlerBase):
    @classmethod
    def add_command(cls, commands):
        parser = commands.add_parser("attributes", help="attributes", epilog=epilog(),
            description="Show attributes.",
            formatter_class=HelpFormatter)

        parser.add_argument("name", metavar="name", type=str, help="test name", default="", nargs="?")
        parser.add_argument("--log", metavar="input", type=argtype.logfile("r", bufsize=1, encoding="utf-8"),
                nargs="?", help="input log, default: stdin", default="-")
        parser.add_argument("--output", metavar="output", type=argtype.file("w", bufsize=1, encoding="utf-8"),
                nargs="?", help='output, default: stdout', default="-")

        parser.set_defaults(func=cls())

    class Pipeline(PipelineBase):
        def __init__(self, name, input, output, tail=False):
            stop_event = threading.Event()

            message_types = [
                Message.ATTRIBUTE.name
            ]

            command = "grep -E '^{\"message_keyword\":\""
            command = f"{command}({'|'.join(message_types)})\""
            command += ".+,\"test_name\":\"%s.*?\",'" % name.replace("'", r"'\''")
            steps = [
                read_and_filter_transform(input, command=command, stop=stop_event, tail=tail),
                parse_transform(),
                sort_transform(stop_event),
                flat_transform(),
                write_transform(output),
            ]
            super(Handler.Pipeline, self).__init__(steps, restart_on_none=False)

    def handle(self, args):
        self.Pipeline(args.name, args.log, args.output).run()