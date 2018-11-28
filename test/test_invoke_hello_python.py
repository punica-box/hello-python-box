#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import time
import unittest

from ontology.ont_sdk import OntologySdk
from ontology.wallet.wallet_manager import WalletManager

from src.invoke_hello_python import InvokeHelloPython

ontology = OntologySdk()
remote_rpc_address = 'http://polaris3.ont.io:20336'
ontology.set_rpc(remote_rpc_address)

root_folder = os.path.dirname(os.path.dirname(__file__))
wallet_path = os.path.join(root_folder, 'wallet', 'wallet.json')
contracts_folder = os.path.join(root_folder, 'contracts')
contract_address_hex = 'f6116319fda70d48f430b9af993f389baa1e94bb'
gas_limit = 20000000
gas_price = 500

wallet_manager = WalletManager()
wallet_manager.open_wallet(wallet_path)
# password = input('password: ')
password = 'password'
acct = wallet_manager.get_account('AKeDu9QW6hfAhwpvCwNNwkEQt1LkUQpBpW', password)
with open(os.path.join(contracts_folder, 'hello_python.abi.json')) as f:
    CONTRACT_ABI = json.loads(f.read())
hello_python = InvokeHelloPython(ontology, CONTRACT_ABI, contract_address_hex)


class TestInvokeSavingPot(unittest.TestCase):
    def test_echo(self):
        msg = 'Hello, Ontology'
        response = hello_python.echo(msg)
        self.assertEqual(msg, response)

    def test_notify_args(self):
        bool_args = True
        int_args = 1024
        list_args = [0, 1, 1024, 2048]
        str_args = 'Hello, Ontology'
        bytes_address_args = acct.get_address().to_array()
        tx_hash = hello_python.notify_args(bool_args, int_args, list_args, str_args, bytes_address_args, acct, acct,
                                           gas_limit, gas_price)
        time.sleep(6)
        event = hello_python.query_notify_args_event(tx_hash)
        self.assertIn(bool_args, event)
        self.assertIn(int_args, event)
        self.assertIn(list_args, event)
        self.assertIn(str_args, event)
        self.assertIn(acct.get_address().b58encode(), event)

    def test_put_list(self):
        list_args = [0, 1, 1024, 2048]
        tx_hash = hello_python.put_list(list_args, acct, acct, gas_limit, gas_price)
        print(tx_hash)

    def test_put_dict(self):
        dict_args = {'key1': 'value1', 'key2': 'value2'}
        tx_hash = hello_python.put_dict(dict_args, acct, acct, gas_limit, gas_price)
        print(tx_hash)

    def test_get_dict(self):
        print(hello_python.get_dict())

    def test_get_list(self):
        print(hello_python.get_list())


if __name__ == '__main__':
    unittest.main()
