from .exchange import get_token_price
import requests


AGGREGATE_VALUES = {
    "1m": ("minute", 1),
    "5m": ("minute", 5),
    "15m": ("minute", 15),
    "1h": ("hour", 1),
    "4h": ("hour", 4),
    "12h": ("hour", 12),
    "1d": ("day", 1),
}


def get_dench_price():
    return get_token_price("DENCH") or 0


def get_dench_ohlcv(period):
    timeframe, aggregate = AGGREGATE_VALUES[period]
    pool_address = "0x45f5dff596a3cccba2b3b84d2e435b139ecfbf07"
    token = "0x2dec733c58388516a1C0E97BBb373dbE906D2797"
    url = "https://api.geckoterminal.com/api/v2/networks/polygon_pos/pools/"
    url += f"{pool_address}/ohlcv/{timeframe}"
    response = requests.get(
        url,
        params={
            "aggregate": aggregate,
            "limit": 100,
            "currency": "usd",
            "token": token,
        },
    )
    return response.json()
