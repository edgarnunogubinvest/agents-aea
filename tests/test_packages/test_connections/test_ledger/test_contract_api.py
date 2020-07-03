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

"""This module contains the tests of the ledger API connection for the contract APIs."""
import asyncio
import json
from pathlib import Path
from typing import cast

import pytest

from aea.configurations.base import (
    ComponentConfiguration,
    ComponentType,
    ContractConfig,
)
from aea.connections.base import Connection
from aea.contracts import contract_registry
from aea.contracts.base import Contract
from aea.crypto.ethereum import EthereumCrypto
from aea.crypto.fetchai import FetchAICrypto
from aea.crypto.wallet import CryptoStore
from aea.helpers.transaction.base import RawTransaction, State
from aea.identity.base import Identity
from aea.mail.base import Envelope

from packages.fetchai.connections.ledger.contract_dispatcher import ContractApiDialogues
from packages.fetchai.protocols.contract_api import ContractApiMessage

from ....conftest import ETHEREUM_ADDRESS_ONE, ROOT_DIR


@pytest.fixture()
async def ledger_apis_connection(request):
    identity = Identity("name", FetchAICrypto().address)
    crypto_store = CryptoStore()
    directory = Path(ROOT_DIR, "packages", "fetchai", "connections", "ledger")
    connection = Connection.from_dir(
        directory, identity=identity, crypto_store=crypto_store
    )
    connection = cast(Connection, connection)
    await connection.connect()
    yield connection
    await connection.disconnect()


@pytest.fixture()
def load_erc1155_contract():
    directory = Path(ROOT_DIR, "packages", "fetchai", "contracts", "erc1155")
    configuration = ComponentConfiguration.load(ComponentType.CONTRACT, directory)
    configuration._directory = directory
    configuration = cast(ContractConfig, configuration)

    # TODO some other tests don't deregister contracts from the registry.
    #   find a neater solution.
    if configuration.public_id in contract_registry.specs.keys():
        contract_registry.specs.pop(str(configuration.public_id))

    # load contract into sys modules!
    Contract.from_config(configuration)

    path = Path(configuration.directory, configuration.path_to_contract_interface)
    with open(path, "r") as interface_file:
        contract_interface = json.load(interface_file)

    contract_registry.register(
        id_=str(configuration.public_id),
        entry_point=f"{configuration.prefix_import_path}.contract:{configuration.class_name}",
        class_kwargs={"contract_interface": contract_interface},
        contract_config=configuration,
    )
    yield
    contract_registry.specs.pop(str(configuration.public_id))


@pytest.mark.network
@pytest.mark.asyncio
async def test_erc1155_get_deploy_transaction(
    load_erc1155_contract, ledger_apis_connection
):
    """Test get state with contract erc1155."""
    address = ETHEREUM_ADDRESS_ONE
    contract_api_dialogues = ContractApiDialogues()
    request = ContractApiMessage(
        performative=ContractApiMessage.Performative.GET_DEPLOY_TRANSACTION,
        dialogue_reference=contract_api_dialogues.new_self_initiated_dialogue_reference(),
        ledger_id=EthereumCrypto.identifier,
        contract_id="fetchai/erc1155:0.6.0",
        callable="get_deploy_transaction",
        kwargs=ContractApiMessage.Kwargs({"deployer_address": address}),
    )
    request.counterparty = str(ledger_apis_connection.connection_id)
    contract_api_dialogue = contract_api_dialogues.update(request)
    assert contract_api_dialogue is not None
    envelope = Envelope(
        to=str(ledger_apis_connection.connection_id),
        sender=address,
        protocol_id=request.protocol_id,
        message=request,
    )

    await ledger_apis_connection.send(envelope)
    await asyncio.sleep(0.01)
    response = await ledger_apis_connection.receive()

    assert response is not None
    assert type(response.message) == ContractApiMessage
    response_message = cast(ContractApiMessage, response.message)
    assert (
        response_message.performative == ContractApiMessage.Performative.RAW_TRANSACTION
    ), "Error: {}".format(response_message.message)
    response_dialogue = contract_api_dialogues.update(response_message)
    assert response_dialogue == contract_api_dialogue
    assert type(response_message.raw_transaction) == RawTransaction
    assert response_message.raw_transaction.ledger_id == EthereumCrypto.identifier
    assert len(response.message.raw_transaction.body) == 6
    assert len(response.message.raw_transaction.body["data"]) > 0


@pytest.mark.network
@pytest.mark.asyncio
async def test_erc1155_get_raw_transaction(
    load_erc1155_contract, ledger_apis_connection
):
    """Test get state with contract erc1155."""
    address = ETHEREUM_ADDRESS_ONE
    contract_address = ETHEREUM_ADDRESS_ONE
    contract_api_dialogues = ContractApiDialogues()
    request = ContractApiMessage(
        performative=ContractApiMessage.Performative.GET_RAW_TRANSACTION,
        dialogue_reference=contract_api_dialogues.new_self_initiated_dialogue_reference(),
        ledger_id=EthereumCrypto.identifier,
        contract_id="fetchai/erc1155:0.6.0",
        contract_address=contract_address,
        callable="get_create_batch_transaction",
        kwargs=ContractApiMessage.Kwargs(
            {"deployer_address": address, "token_ids": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]}
        ),
    )
    request.counterparty = str(ledger_apis_connection.connection_id)
    contract_api_dialogue = contract_api_dialogues.update(request)
    assert contract_api_dialogue is not None
    envelope = Envelope(
        to=str(ledger_apis_connection.connection_id),
        sender=address,
        protocol_id=request.protocol_id,
        message=request,
    )

    await ledger_apis_connection.send(envelope)
    await asyncio.sleep(0.01)
    response = await ledger_apis_connection.receive()

    assert response is not None
    assert type(response.message) == ContractApiMessage
    response_message = cast(ContractApiMessage, response.message)
    assert (
        response_message.performative == ContractApiMessage.Performative.RAW_TRANSACTION
    ), "Error: {}".format(response_message.message)
    response_dialogue = contract_api_dialogues.update(response_message)
    assert response_dialogue == contract_api_dialogue
    assert type(response_message.raw_transaction) == RawTransaction
    assert response_message.raw_transaction.ledger_id == EthereumCrypto.identifier
    assert len(response.message.raw_transaction.body) == 7
    assert len(response.message.raw_transaction.body["data"]) > 0


@pytest.mark.network
@pytest.mark.asyncio
async def test_erc1155_get_state(load_erc1155_contract, ledger_apis_connection):
    """Test get state with contract erc1155."""
    address = ETHEREUM_ADDRESS_ONE
    contract_address = "0x250A2aeb3eB84782e83365b4c42dbE3CDA9920e4"
    contract_api_dialogues = ContractApiDialogues()
    token_id = 1
    request = ContractApiMessage(
        performative=ContractApiMessage.Performative.GET_STATE,
        dialogue_reference=contract_api_dialogues.new_self_initiated_dialogue_reference(),
        ledger_id=EthereumCrypto.identifier,
        contract_id="fetchai/erc1155:0.6.0",
        contract_address=contract_address,
        callable="get_balance",
        kwargs=ContractApiMessage.Kwargs(
            {"agent_address": address, "token_id": token_id}
        ),
    )
    request.counterparty = str(ledger_apis_connection.connection_id)
    contract_api_dialogue = contract_api_dialogues.update(request)
    assert contract_api_dialogue is not None
    envelope = Envelope(
        to=str(ledger_apis_connection.connection_id),
        sender=address,
        protocol_id=request.protocol_id,
        message=request,
    )

    await ledger_apis_connection.send(envelope)
    await asyncio.sleep(0.01)
    response = await ledger_apis_connection.receive()

    assert response is not None
    assert type(response.message) == ContractApiMessage
    response_message = cast(ContractApiMessage, response.message)
    assert (
        response_message.performative == ContractApiMessage.Performative.STATE
    ), "Error: {}".format(response_message.message)
    response_dialogue = contract_api_dialogues.update(response_message)
    assert response_dialogue == contract_api_dialogue
    assert type(response_message.state) == State
    assert response_message.state.ledger_id == EthereumCrypto.identifier
    result = response_message.state.body.get("balance", None)
    expected_result = {token_id: 0}
    assert result is not None and result == expected_result
