from pprint import pprint

from web3 import Web3
import requests
from MetamaskConnectionAbstract import MetamaskConnectionAbstract

url_eth = "https://api.bscscan.com/api"
wallet_address = "0xaff2C41Cb30869D16054F3Dc55896905acA7EFd3"
token_address = "0x62aa52175ff697989b214b298cef5053b0bfdef6"
contract_address = Web3.toChecksumAddress(token_address)
api_key = "UX5ZX68Z24A8PNS5HJV2R2IYBIVCCCPF4X"
API_ENDPOINT = url_eth + "?module=contract&action=getabi&address=" + str(contract_address) + f"&apikey={api_key}"

results = requests.get(API_ENDPOINT)
# pprint(results.json(), indent=6)
bsc = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))

balance = web3.eth.get_balance(wallet_address)

print(balance)

result = web3.fromWei(balance, "ether")


def get_address_of_buyer():
    pass


TxParams = \
    {
        "from": "0xaff2C41Cb30869D16054F3Dc55896905acA7EFd3",
        "to": "0xd46e8dd67c5d32be8058bb8eb970870f07244567",
        "gas": "0x76c0",  # 30400
        "gasPrice": "0x9184e72a000",  # 10000000000000
        "value": "0x9184e72a",  # 2441406250
        "data": "0xd46e8dd67c5d32be8d46e8dd67c5d32be8058bb8eb970870f072445675058bb8eb970870f072445675"
    }

print(web3.eth.send_transaction(TxParams))

print(result)
exit()


class MetamaskConnection(MetamaskConnectionAbstract):
    def __init__(self, wallet_credentials, url):
        super().__init__(wallet_credentials, url)

    def get_wallet_balance_by_coin(self):
        pass

    def send_coin(self):
        pass

    def get_address_for_coin(self):
        pass
