from api import models
from random import choices
import string

alphabet = string.ascii_letters + string.digits


def get_address_by_pk(token_pk):
    return models.Token.get_address_by_pk(token_pk)


def generate_passcode(address=None):
    passcode = models.UserStaking.return_passcode(address)
    if not passcode:
        passcode = "".join(choices(alphabet, k=20))
    return passcode
