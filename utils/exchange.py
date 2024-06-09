from .token import get_address_by_pk

from urllib.parse import urlencode
import requests

__CURRENCYES = {
    "polygon": {
        "DODO": "0xe4bf2864ebec7b7fdf6eeca9bacae7cdfdaffe78",
        "USDT": "0xc2132d05d31c914a87c6611c10748aeb04b58e8f",
        "USDC": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
        "DAI": "0x8f3cf7ad23cd3cadbd9735aff958023239c6a063",
        "DENCH": "0x2dec733c58388516a1C0E97BBb373dbE906D2797",
    }
}


def get_token_info(token, chain="polygon"):
    if not token:
        return None
    url = "https://api.geckoterminal.com/api/v2/networks/polygon_pos/tokens/"
    url += token
    response = requests.get(url)
    return response.json().get("data", {})


def get_token_price(token_pk, chain="polygon"):
    token = get_address_by_pk(token_pk)
    return float(
        (
            get_token_info(token, chain)
            .get("attributes", {})
            .get("price_usd", 0)
        )
    )


def generate_swap_url(
    from_token=None,
    to_token=None,
    exact_amount=None,
    exact_Field="input",
    chain="polygon",
):
    url = "https://app.uniswap.org/#/swap?"
    if from_token and to_token:
        params = {
            "chain": chain,
            "inputCurrency": get_address_by_pk(from_token),
            "outputCurrency": get_address_by_pk(to_token),
        }
        if exact_amount:
            params["exactAmount"] = exact_amount
            params["exactField"] = exact_Field
        url += urlencode(params)
    return url
