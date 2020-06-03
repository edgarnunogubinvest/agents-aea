# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2020 Fetch.AI Limited
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

"""Implementation of the 'aea interact' subcommand."""

import codecs
from typing import Optional

import click

from aea.cli.utils.exceptions import InterruptInputException
from aea.configurations.base import PublicId
from aea.connections.stub.connection import (
    DEFAULT_INPUT_FILE_NAME,
    DEFAULT_OUTPUT_FILE_NAME,
    StubConnection,
)
from aea.mail.base import Envelope, InBox, Multiplexer, OutBox


@click.command()
def interact():
    """Interact with a running AEA via the stub connection."""
    click.echo("Starting AEA interaction channel...")
    _run_interaction_channel()


def _run_interaction_channel():
    stub_connection = StubConnection(
        input_file_path=DEFAULT_OUTPUT_FILE_NAME,
        output_file_path=DEFAULT_INPUT_FILE_NAME,
    )
    multiplexer = Multiplexer([stub_connection])
    inbox = InBox(multiplexer)
    outbox = OutBox(multiplexer)

    try:
        multiplexer.connect()
        is_running = True
        while is_running:
            try:
                envelope = _try_construct_envelope()
                if envelope is None and not inbox.empty():
                    envelope = inbox.get_nowait()
                    assert (
                        envelope is not None
                    ), "Could not recover envelope from inbox."
                    click.echo(_construct_message("received", envelope))
                elif envelope is None and inbox.empty():
                    click.echo("Received no new envelope!")
                else:
                    outbox.put(envelope)
                    click.echo(_construct_message("sending", envelope))
            except KeyboardInterrupt:
                is_running = False
            except Exception as e:
                click.echo(e)
    finally:
        multiplexer.disconnect()


def _construct_message(action_name, envelope):
    action_name = action_name.title()
    message = (
        "{} envelope:\nto: "
        "{}\nsender: {}\nprotocol_id: {}\nmessage: {}\n".format(
            action_name,
            envelope.to,
            envelope.sender,
            envelope.protocol_id,
            envelope.message,
        )
    )
    return message


def _try_construct_envelope() -> Optional[Envelope]:
    """Try construct an envelope from user input."""
    envelope = None  # type: Optional[Envelope]
    try:
        click.echo("Provide envelope to:")
        to = input()  # nosec
        if to == "":
            raise InterruptInputException
        click.echo("Provide envelope sender:")
        sender = input()  # nosec
        if sender == "":
            raise InterruptInputException
        click.echo("Provide envelope protocol_id:")
        protocol_id = input()  # nosec
        if protocol_id == "":
            raise InterruptInputException
        click.echo("Provide envelope message:")
        message_escaped = input()  # nosec
        if message_escaped == "":
            raise InterruptInputException
        message = codecs.decode(message_escaped.encode("utf-8"), "unicode-escape")
        message_encoded = message.encode("utf-8")
        envelope = Envelope(
            to=to,
            sender=sender,
            protocol_id=PublicId.from_str(protocol_id),
            message=message_encoded,
        )
    except InterruptInputException:
        click.echo("Interrupting input, checking inbox ...")
    except KeyboardInterrupt as e:
        raise e
    except Exception as e:
        click.echo(e)
    return envelope