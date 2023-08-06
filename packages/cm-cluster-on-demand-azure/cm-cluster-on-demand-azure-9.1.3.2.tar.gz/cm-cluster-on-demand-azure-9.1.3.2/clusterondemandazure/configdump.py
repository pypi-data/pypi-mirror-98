# Copyright 2004-2021 Bright Computing Holding BV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import absolute_import, print_function

import clusterondemand.configdump
from clusterondemand.configuration import get_enforcing_config_files, get_system_config_files
from clusterondemandconfig import ConfigNamespace, config, full_ini_config_dump, load_configuration_for_parameters

COMMAND_HELP_TEXT = clusterondemand.configdump.COMMAND_HELP_TEXT

config_ns = ConfigNamespace("azure.config.dump")
config_ns.import_namespace(clusterondemand.configuration.common_ns)


def run_command():
    from .cli import azure_commands

    config_to_dump = load_configuration_for_parameters(
        azure_commands.parameters(),
        system_config_files=get_system_config_files(),
        enforcing_config_files=get_enforcing_config_files()
    )
    print(full_ini_config_dump(config_to_dump, show_secrets=config["show_secrets"]))
