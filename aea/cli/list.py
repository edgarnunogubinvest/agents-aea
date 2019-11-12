# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""Implementation of the 'aea list' subcommand."""
import os

import click


from aea.cli.common import Context, pass_ctx, _try_to_load_agent_config, retrieve_description
from aea.configurations.base import DEFAULT_AEA_CONFIG_FILE, DEFAULT_CONNECTION_CONFIG_FILE, DEFAULT_SKILL_CONFIG_FILE, \
    DEFAULT_PROTOCOL_CONFIG_FILE


@click.group()
@pass_ctx
def list(ctx: Context):
    """List the installed resources."""
    _try_to_load_agent_config(ctx)


@list.command()
@pass_ctx
def connections(ctx: Context):
    """List all the installed connections."""
    for connection_id in sorted(ctx.agent_config.connections):
        connection_configuration_filepath = os.path.join("connections", connection_id, DEFAULT_CONNECTION_CONFIG_FILE)
        print("{}\t[{}]".format(connection_id, retrieve_description(ctx.connection_loader, connection_configuration_filepath)))


@list.command()
@pass_ctx
def protocols(ctx: Context):
    """List all the installed protocols."""
    for protocol_id in sorted(ctx.agent_config.protocols):
        protocol_configuration_filepath = os.path.join("protocols", protocol_id, DEFAULT_PROTOCOL_CONFIG_FILE)
        print("{}\t[{}]".format(protocol_id, retrieve_description(ctx.protocol_loader, protocol_configuration_filepath)))


@list.command()
@pass_ctx
def skills(ctx: Context):
    """List all the installed skills."""
    for skill_id in sorted(ctx.agent_config.skills):
        skill_configuration_filepath = os.path.join("skills", skill_id, DEFAULT_SKILL_CONFIG_FILE)
        print("{}\t[{}]".format(skill_id, retrieve_description(ctx.skill_loader, skill_configuration_filepath)))
