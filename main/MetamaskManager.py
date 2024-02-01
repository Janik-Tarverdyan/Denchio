import json
import time
from random import choices

import requests
from web3 import Web3
from ethtoken.abi import EIP20_ABI

from coinpaprika import client as cp

import string
from main.DBTableManager import TableManager


class MetamaskManager:
    counter = 0

    @staticmethod
    def get_coin_name_by_chain(expected_coin, chain_type):
        coin_name = expected_coin
        if 'ERC' in chain_type:
            coin_name += "-ERC"
        return coin_name

    @staticmethod
    def get_coin_map():
        coin_map = {
            'DODO': 'dodo-dodo',
            'DENCH': 'dench-denchcoin',
            'BUSD': 'busd-binance-usd',
            'USDC': 'usdc-usd-coin',
            'USDT': 'usdt-tether',
            'CAKE': 'cake-pancakeswap',
        }
        return coin_map

    @staticmethod
    def get_price(to_coin="USD"):
        client = cp.Client()
        coin_map = MetamaskManager.get_coin_map()
        try:
            price = None
            if "USD" in to_coin:
                price = round(client.ticker("dench-denchcoin")['quotes']['USD']['price'], 3)
            else:
                if to_coin in coin_map.keys():
                    price_base_usd = round(client.ticker(coin_map[to_coin])['quotes']['USD']['price'], 3)
                    price_dench_usd = round(client.ticker("dench-denchcoin")['quotes']['USD']['price'], 3)
                    price = round(price_dench_usd / price_base_usd, 3)
        except Exception as e:
            print(e)
            price = 0.0
        return price

    @staticmethod
    def get_price_usd(from_coin):
        client = cp.Client()
        coin_map = MetamaskManager.get_coin_map()
        if from_coin in coin_map.keys():
            price_base_usd = round(client.ticker(coin_map[from_coin])['quotes']['USD']['price'], 5)
            return price_base_usd

    @staticmethod
    def pair_TokenLP_amount(tx_pair):
        print(float(tx_pair[1]['called_amount']) * MetamaskManager.get_price_usd(tx_pair[1]['coin']))
        return float(tx_pair[1]['called_amount']) * MetamaskManager.get_price_usd(tx_pair[1]['coin'])

    @staticmethod
    def calculate_coin_vs_transaction_diff(tx_info, called_params):
        called_pair_ratio = float(called_params['base_amount']) / float(called_params['quote_amount'])
        transaction_ratio = float(tx_info['base_amount']) / float(tx_info['quote_amount'])
        if abs(transaction_ratio - called_pair_ratio) / called_pair_ratio < 0.01:
            return True
        else:
            return False

    @staticmethod
    def calculate_coin_amount(tx_amount, called_params):
        price = float(called_params['price'])
        if abs(float(called_params['coin_amount']) - float(tx_amount) / float(price)) < 0.022:
            return float(called_params['coin_amount'])
        return 0

    @staticmethod
    def get_paired_transfers(tx_combo_details_base, tx_combo_details_quote, called_params):
        tx_combo_paired = []
        for tx_base in tx_combo_details_base:
            if abs(float(tx_base['called_amount']) - float(tx_base['amount'])) / float(tx_base['amount']) < 0.01:
                for tx_quote in tx_combo_details_quote:
                    print(float(tx_quote['amount']))
                    if abs(float(tx_quote['called_amount']) - float(tx_quote['amount'])) / float(
                            tx_quote['called_amount']) < 0.011 and tx_base['from'] == tx_quote['from']:
                        if MetamaskManager.calculate_coin_vs_transaction_diff(
                                {'base_amount': float(tx_base['amount']), 'quote_amount': float(tx_quote['amount'])},
                                called_params):
                            tx_combo_paired.append([tx_base, tx_quote])
        return tx_combo_paired

    @staticmethod
    def get_tx_details(transaction_details, called_params):
        tx_combo_details = []
        for tx_hash in transaction_details:
            tx_detail = transaction_details[tx_hash]
            tx_detail.update({"tx_hash": tx_hash})
            if tx_detail['coin'] == called_params['base']:
                tx_detail.update({"called_amount": called_params['base_amount']})
            elif tx_detail['coin'] == called_params['quote']:
                tx_detail.update({"called_amount": called_params['quote_amount']})
            tx_combo_details.append(tx_detail)
        return tx_combo_details

    def __init__(self, address, private_key):

        self.bsc = "https://bsc-dataseed.binance.org/"
        self.w3 = Web3(Web3.HTTPProvider(self.bsc))
        self.wallet_address = address
        self.bsc_api_key = "UX5ZX68Z24A8PNS5HJV2R2IYBIVCCCPF4X"
        self.bsc_api_url = "https://api.bscscan.com/api"
        self._contract_address = {"BUSD": self.w3.toChecksumAddress('0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56'),
                                  "DENCH": self.w3.toChecksumAddress("0x62aa52175ff697989b214b298cef5053b0bfdef6"),
                                  "DODO": self.w3.toChecksumAddress("0x67ee3cb086f8a16f34bee3ca72fad36f7db929e2"),
                                  # 0x43Dfc4159D86F3A37A5A4B3D4580b888ad7d4DDd
                                  "USDD": self.w3.toChecksumAddress("0xfca55597b4be2b864576085c7f8dd01663904c30"),
                                  "TOKENLP": self.w3.toChecksumAddress("0xffcbf30359eaf4a08c717b47730f85c2f9028dc8"),
                                  "CAKE": self.w3.toChecksumAddress("0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82"),
                                  }
        self._contract_address_eth = {
            "USDT-ERC": self.w3.toChecksumAddress("0xdAC17F958D2ee523a2206206994597C13D831ec7"),
            "USDC-ERC": self.w3.toChecksumAddress("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"),
            "DENCH-ERC": self.w3.toChecksumAddress("0x4b7265d153886a7dc717e815862acde6ff7b5bc8"),
            "DODO-ERC": self.w3.toChecksumAddress("0x43Dfc4159D86F3A37A5A4B3D4580b888ad7d4DDd")
        }

        self.ABIs = self.generate_abi_bsc()

        self.contracts = self.generate_contracts_bsc()
        self.contracts.update(self.generate_contracts_eth())
        self.private_key = private_key
        self.event_list = []
        self.counter += 1

    def get_abi(self, contract_address):
        result = requests.get(url=self.get_endpoint_by_contract_bsc(contract_address))
        response = result.json()
        abi = json.loads(response["result"])
        return abi

    def generate_abi_bsc(self):
        ABIs = {}
        for key in self._contract_address:
            ABIs.update({key: self.get_abi(self._contract_address[key])})
        return ABIs

    def generate_contracts_bsc(self):
        contracts = {}
        for key in self._contract_address:
            if key in self.ABIs.keys():
                contracts.update({key: self.w3.eth.contract(address=self._contract_address[key], abi=self.ABIs[key])})
        return contracts

    def generate_contracts_eth(self):
        contracts = {}
        for key in self._contract_address_eth:
            if key in self.ABIs.keys():
                contracts.update({key: self.w3.eth.contract(address=self._contract_address_eth[key], abi=EIP20_ABI)})
        return contracts

    def get_endpoint_by_contract_bsc(self, contract_address):
        api_endpoint = self.bsc_api_url + "?module=contract&action=getabi&address=" + str(
            contract_address) + f"&apikey={self.bsc_api_key}"
        return api_endpoint

    def get_tx_info(self, transaction_address):
        info = self.w3.eth.getTransaction(transaction_address)
        abi = self.get_abi(info['to'])
        contract_for_transaction = self.w3.eth.contract(address=info['to'], abi=abi)
        # print(info)
        symbol = contract_for_transaction.functions.symbol().call()
        # print(f"coin : {contract_for_transaction.functions.name().call()}")
        # print(f"symbol : {symbol}")

        func_obj, func_params = contract_for_transaction.decode_function_input(info["input"])
        # print(func_params)
        # print(func_params)
        coins = 0
        if symbol == "DENCH":
            coins = self.w3.fromWei(func_params['tokens'], 'ether')
        else:
            if 'amount' in func_params.keys():
                coins = self.w3.fromWei(func_params['amount'], 'ether')

        if 'to' in func_params.keys() and 'recipient' not in func_params.keys():
            func_params['recipient'] = func_params['to']
        # self.w3.eth.get_block(block_identifier=info.blockNumber).timestamp,
        return {'from': info['from'], 'to': func_params['recipient'], 'amount': coins, 'coin': symbol}

    def send_transaction(self, transaction, to_address, coins):
        signed_txn = self.w3.eth.account.signTransaction(transaction, private_key=self.private_key)
        try:
            tx_hash = self.w3.eth.sendRawTransaction(signed_txn.rawTransaction)
            txid = self.w3.toHex(tx_hash)
            return [txid, 'Success']
        except Exception as e:
            print(e)
            print(transaction)
            print("reference for fix :", to_address, coins)
            return [0, 'Failed']

    def send_dench_to_address(self, to_address, coin_amount, coin_chain):
        nonce = self.w3.eth.getTransactionCount(self.wallet_address)
        coin_name = self.get_coin_name_by_chain('DENCH', coin_chain)
        coins = self.w3.toWei(coin_amount, "ether")
        transaction = self.contracts[coin_name].functions.transfer(to_address, coins).buildTransaction(
            {'gas': 50000 * 2, 'nonce': nonce})

        return self.send_transaction(transaction, to_address, coins)

    def send_coin_to_address(self, to_address, coin_name, coin_amount):
        nonce = self.w3.eth.getTransactionCount(self.wallet_address)

        coins = self.w3.toWei(coin_amount, "ether")
        # print(self.w3.eth.getBlock("latest").gasLimit)
        if coin_name not in self.contracts.keys():
            raise Exception("Coin name is not in the contract list", coin_name, self.contracts.keys())
        transaction = self.contracts[coin_name].functions.transfer(to_address, coins).buildTransaction(
            {'gas': 50000 * 2, 'nonce': nonce})
        # print(web3.eth.send_transaction(transaction))
        return self.send_transaction(transaction, to_address, coins)

    def get_transaction_estimated_fee(self, to_address, coin_amount):
        print(f"gas_price: {self.w3.eth.gasPrice}")
        print(self.w3.fromWei(self.w3.eth.estimateGas(
            {'from': self.wallet_address, 'to': to_address, "amount": self.w3.toWei(coin_amount, "ether")}), "ether"))
        return self.w3.eth.gasPrice * self.w3.fromWei(self.w3.eth.estimateGas(
            {'from': self.wallet_address, 'to': to_address, "amount": self.w3.toWei(coin_amount, "ether")}), "ether")

    def get_last_transactions(self, coin_name):
        """
        [AttributeDict({'args': AttributeDict(
                       'to': '0xd589E5E40A27798390a3436e3A52144c4cB96037',
                       'tokens': 1000000000000000000}),
                       'event': 'Transfer',
                       'logIndex': 289,
                       'transactionIndex': 94,
                       'transactionHash':HexBytes('0xd4fa81cb0805079158e44a191bd85228ed93305983116b8909aef97f7f4641e1'),
                       'address': '0x62aA52175Ff697989B214b298cEF5053B0bFdEF6',
                       'blockHash': HexBytes('0x3ef7935819027cba4d2605ea7a88971230d399efce9143dbae4d9b1e74addf77'),
                       'blockNumber': 11205591})]
        """
        if coin_name not in self.contracts.keys():
            return {}
        latest = self.w3.eth.blockNumber

        transfer_events = self.contracts[coin_name.upper()].events.Transfer.createFilter(fromBlock=latest - 4999,
                                                                                         toBlock=latest,
                                                                                         argument_filters={
                                                                                             'to': self.wallet_address})
        received = {}
        for tx in transfer_events.get_all_entries():
            new_transaction = self.get_tx_info(tx.transactionHash)
            received.update({tx.transactionHash: new_transaction})
        return received

    def reply_to_transaction(self, transaction_detail, calculate_amount, coin_chain):
        send_back_to = transaction_detail['from']
        print(send_back_to)

        meta_db = TableManager("meta", "./db.sqlite3")
        if not meta_db.exists_for_transaction(transaction_detail):
            result = self.send_dench_to_address(send_back_to, calculate_amount, coin_chain)
            if result[1] == 'Failed':
                return result
            result = [0, "Success"]
            meta_db.insert_element_for_transaction(transaction_detail)
            return result
        else:
            return [0, "Transaction already done successfully"]

    def catching_loop_of_transaction(self, called_params):
        check = False
        for _ in range(10):
            try:
                coin_name = self.get_coin_name_by_chain(called_params['expected_coin'], called_params['chain_type'])
                transaction_details = self.get_last_transactions(coin_name)
                result = None
                for tx_hash in transaction_details:
                    transaction_detail = transaction_details[tx_hash]
                    transaction_detail.update({"tx_hash": tx_hash})
                    calculate_amount = self.calculate_coin_amount(transaction_detail['amount'],
                                                                  called_params)
                    if calculate_amount != 0:
                        result = self.reply_to_transaction(transaction_detail, calculate_amount,
                                                           called_params['chain_type'])
                    else:
                        result = [0, 'Failed']

                if result and result[1] == 'Success':
                    return 'Success'
                elif result and "Transaction" in result[1]:
                    return result[1]
                time.sleep(2)
                if not result:
                    check = True
            except Exception as e:
                print(e)
        if check:
            return 'Transaction cannot be found'
        return 'Failed : Internal Error: Transaction will be fixed within a day.'

    def catching_loop_of_paired_transaction(self, called_params):
        for _ in range(10):
            try:
                chain_type = called_params['chain_type']
                base_coin_name = self.get_coin_name_by_chain(called_params['base'], chain_type)
                quote_coin_name = self.get_coin_name_by_chain(called_params['quote'], chain_type)

                transaction_details_base = self.get_last_transactions(base_coin_name)
                transaction_details_quote = self.get_last_transactions(quote_coin_name)
                tx_combo_details_base = self.get_tx_details(transaction_details_base, called_params)
                tx_combo_details_quote = self.get_tx_details(transaction_details_quote, called_params)
                tx_pairs = self.get_paired_transfers(tx_combo_details_base, tx_combo_details_quote, called_params)
                for tx_pair in tx_pairs:
                    print(tx_pair)
                    result = self.reply_to_paired_transaction(tx_pair, called_params['apr'], chain_type)
                    if result and 'Success' in result[1]:
                        return result[1]
                    time.sleep(2)
            except Exception as e:
                print(e)
                return 'Failed : Internal Error: Transaction will be fixed within a day.'
        return 'Transaction cannot be found'

    def reply_to_paired_transaction(self, tx_pair, apr, chain_type):
        send_back_to = tx_pair[0]['from']
        print(send_back_to)
        db = TableManager("paired_transactions_final", "./db.sqlite3")
        if not db.exists_for_pair(tx_pair):
            if db.exists_account(send_back_to):
                passcode = db.get_passcode(send_back_to)
            else:
                alphabet = string.ascii_letters + string.digits
                passcode = ''.join(choices(alphabet, k=20))
                print("passcode:", passcode)
            calculate_amount = self.pair_TokenLP_amount(tx_pair)
            result = self.send_coin_to_address(send_back_to, "TOKENLP", calculate_amount)
            if result[1] == 'Failed':
                return result
            result[1] = "Success, Please keep the passcode for future use. The passcode is  : %s" % passcode
            db.insert_element_for_pair(tx_pair, apr, passcode, calculate_amount, chain_type)
            return result

    def catching_loop_of_resign_contract(self, called_params):
        check = False
        for _ in range(10):
            try:
                db = TableManager("paired_transactions_final", "./db.sqlite3")
                transaction_info = db.get_pairs_full_info_for_resign(called_params['wallet_address'],
                                                                     called_params['passcode'],
                                                                     called_params['index'])

                transaction_details = self.get_last_transactions(called_params['expected_coin'])
                result = None
                for tx_hash in transaction_details:
                    transaction_detail = transaction_details[tx_hash]
                    transaction_detail.update({"tx_hash": tx_hash})
                    ratio = abs(float(transaction_info[5]) / float(transaction_detail['amount']) - 1)
                    if ratio < 0.01 and transaction_detail['amount'].upper() == called_params['wallet_address'].upper():
                        result = self.resign_contract(db, transaction_info, called_params)
                    else:
                        result = [0, 'Failed']

                if result and result[1] == 'Success':
                    return 'Success'
                elif result and "Transaction" in result[1]:
                    return result[1]
                time.sleep(2)
                if not result:
                    check = True
            except Exception as e:
                print(e)
        if check:
            return 'Transaction cannot be found'
        return 'Failed : Internal Error: Transaction will be fixed within a day.'

    def resign_contract(self, db, transaction_info, called_params):
        send_back_to = called_params['wallet_address']
        if db.contract_exists(transaction_info, called_params):
            result = self.send_coin_to_address(send_back_to, transaction_info[0], transaction_info[3])
            result1 = self.send_coin_to_address(send_back_to, transaction_info[1], transaction_info[4])
            if result[1] == 'Failed' or result1 == 'Failed':
                return result
            result[1] = "Success, The contract is resigned."
            db.drop_contract(transaction_info, called_params)
            return result


if __name__ == "__main__":
    to_addr = "0xd589E5E40A27798390a3436e3A52144c4cB96037"
    addr = "0xa1e453b2c576acEEA6d406b7366536feB8A6DF55"
    test = "0xad2ed3a0b94a9b369b0fe8cd031b2d0932600ee3139817c73885074e0c267b82"
    test1 = "0x9e0507cc08f09a7b28ae845116699864935f5d225b1839e565669bb4ce43bc95"
    test2 = "0xb26b30b2ddc482f698cafa8668a09351a7e1daac40eddfdf9b13011cac0f0ea8"
    test3 = "0x268c844a2c1d6ff1ab3a70249eb575417f090946cd5364ea9fb87a7fdcc0328f"
    p_key = "34dfb81837d00d9b5992d911caaeeda19a76015ef74ad88d018f7badbae1e3e4"
    metaMask = MetamaskManager(addr, p_key)
    # print(metaMask.get_tx_info(test))
    # print(metaMask.get_tx_info(test1))
    # print(metaMask.get_tx_info(test2))
    # print(metaMask.get_tx_info(test3))
    # print(metaMask.get_transaction_estimated_fee(to_address, 1))
    # transaction_id = metaMask.send_dench_to_address(to_address, 1)
    # metaMask.get_tx_info(transaction_id)
    # metaMask.catching_loop_of_transaction({"coin_amount": 0.0000409})
    # for i in metaMask.get_last_transactions():
    #     print(i)
    # print(metaMask.get_transaction_estimated_fee(to_addr, 2))
