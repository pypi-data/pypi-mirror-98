# -*- coding: utf-8 -*-

# Copyright 2010-2020 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import sys

from cliff.app import App
from cliff.commandmanager import CommandManager


class SushyCliApp(App):
    """Cliff application for the `sushycli` tool.

    :param description: one-liner explaining the program purpose
    :param version: application version number
    :param command_manager: plugin loader
    :param deferred_help: Allow subcommands to accept `–help` with allowing
        to defer help print after initialize_app
    """

    def __init__(self):
        super(SushyCliApp, self).__init__(
            description='Redfish CLI based on sushy library',
            version='0.1',
            command_manager=CommandManager('sushycli'),
            deferred_help=True)

    def initialize_app(self, argv):
        self.LOG.debug('initialize_app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('prepare_to_run_command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('clean_up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    myapp = SushyCliApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
