# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2020 fetchai
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

"""
This module contains the classes required for t_protocol_no_ct dialogue management.

- TProtocolNoCtDialogue: The dialogue class maintains state of a dialogue and manages it.
- TProtocolNoCtDialogues: The dialogues class keeps track of all dialogues.
"""

from abc import ABC
from typing import Callable, FrozenSet, Type, cast

from aea.common import Address
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, DialogueLabel, Dialogues

from tests.data.generator.t_protocol_no_ct.message import TProtocolNoCtMessage


class TProtocolNoCtDialogue(Dialogue):
    """The t_protocol_no_ct dialogue class maintains state of a dialogue and manages it."""

    INITIAL_PERFORMATIVES = frozenset(
        {TProtocolNoCtMessage.Performative.PERFORMATIVE_PT}
    )
    TERMINAL_PERFORMATIVES = frozenset(
        {
            TProtocolNoCtMessage.Performative.PERFORMATIVE_MT,
            TProtocolNoCtMessage.Performative.PERFORMATIVE_O,
            TProtocolNoCtMessage.Performative.PERFORMATIVE_EMPTY_CONTENTS,
        }
    )
    VALID_REPLIES = {
        TProtocolNoCtMessage.Performative.PERFORMATIVE_EMPTY_CONTENTS: frozenset(
            {TProtocolNoCtMessage.Performative.PERFORMATIVE_EMPTY_CONTENTS}
        ),
        TProtocolNoCtMessage.Performative.PERFORMATIVE_MT: frozenset(),
        TProtocolNoCtMessage.Performative.PERFORMATIVE_O: frozenset(),
        TProtocolNoCtMessage.Performative.PERFORMATIVE_PCT: frozenset(
            {
                TProtocolNoCtMessage.Performative.PERFORMATIVE_MT,
                TProtocolNoCtMessage.Performative.PERFORMATIVE_O,
            }
        ),
        TProtocolNoCtMessage.Performative.PERFORMATIVE_PMT: frozenset(
            {
                TProtocolNoCtMessage.Performative.PERFORMATIVE_MT,
                TProtocolNoCtMessage.Performative.PERFORMATIVE_O,
            }
        ),
        TProtocolNoCtMessage.Performative.PERFORMATIVE_PT: frozenset(
            {
                TProtocolNoCtMessage.Performative.PERFORMATIVE_PT,
                TProtocolNoCtMessage.Performative.PERFORMATIVE_PCT,
                TProtocolNoCtMessage.Performative.PERFORMATIVE_PMT,
            }
        ),
    }

    class Role(Dialogue.Role):
        """This class defines the agent's role in a t_protocol_no_ct dialogue."""

        ROLE_1 = "role_1"
        ROLE_2 = "role_2"

    class EndState(Dialogue.EndState):
        """This class defines the end states of a t_protocol_no_ct dialogue."""

        END_STATE_1 = 0
        END_STATE_2 = 1
        END_STATE_3 = 2

    def __init__(
        self,
        dialogue_label: DialogueLabel,
        self_address: Address,
        role: Dialogue.Role,
        message_class: Type[TProtocolNoCtMessage] = TProtocolNoCtMessage,
    ) -> None:
        """
        Initialize a dialogue.

        :param dialogue_label: the identifier of the dialogue
        :param self_address: the address of the entity for whom this dialogue is maintained
        :param role: the role of the agent this dialogue is maintained for
        :return: None
        """
        Dialogue.__init__(
            self,
            dialogue_label=dialogue_label,
            message_class=message_class,
            self_address=self_address,
            role=role,
        )


class TProtocolNoCtDialogues(Dialogues, ABC):
    """This class keeps track of all t_protocol_no_ct dialogues."""

    END_STATES = frozenset(
        {
            TProtocolNoCtDialogue.EndState.END_STATE_1,
            TProtocolNoCtDialogue.EndState.END_STATE_2,
            TProtocolNoCtDialogue.EndState.END_STATE_3,
        }
    )

    def __init__(
        self,
        agent_address: Address,
        role_from_first_message: Callable[[Message, Address], Dialogue.Role],
        dialogue_class: Type[TProtocolNoCtDialogue] = TProtocolNoCtDialogue,
    ) -> None:
        """
        Initialize dialogues.

        :param agent_address: the address of the agent for whom dialogues are maintained
        :return: None
        """
        Dialogues.__init__(
            self,
            agent_address=agent_address,
            end_states=cast(FrozenSet[Dialogue.EndState], self.END_STATES),
            message_class=TProtocolNoCtMessage,
            dialogue_class=dialogue_class,
            role_from_first_message=role_from_first_message,
        )
