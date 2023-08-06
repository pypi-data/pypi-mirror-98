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

from sushycli import base


class VersionShow(base.BaseLister):
    """Show Redfish protocol version implemented by the BMC

    Implements `sushycli version show` command.
    """
    def get_parser(self, prog_name):
        """Redfish version command parser.

        :param prog_name: name of the cliff command being executed
        :returns: an `argparse.ArgumentParser` instance
        """
        parser = super(VersionShow, self).get_parser(prog_name)

        return parser

    def take_action(self, args):
        """Redfish version command action

        :param args: a namespace of command-line option-value pairs that
            come from the user
        :returns: CLI process exit code
        """
        root = super(VersionShow, self).take_action(args)

        return ['Version'], [[root.redfish_version]]
