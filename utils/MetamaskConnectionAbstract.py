# from web3 import Web3
from abc import ABC, abstractmethod


class MetamaskConnectionAbstract(ABC):
    def __init__(self, wallet_credentials, url):
        self.wallet_credentials = wallet_credentials
        self.url = url
        pass

    @abstractmethod
    def get_wallet_balance_by_coin(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def send_coin(self, coin_type, amount) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_address_for_coin(self, coin_type) -> str:
        raise NotImplementedError
