from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
from datetime import datetime

from .models import Staking, UserStaking

from utils import denchcoin
from utils.token import generate_passcode
from utils.exchange import get_token_price, generate_swap_url

from polygonscan import PolygonScan

import json


def get_price(request):
    return JsonResponse({"price": denchcoin.get_dench_price()})


def get_chart(request):
    response = denchcoin.get_dench_ohlcv(request.GET.get("type", "5m"))
    labels = []
    chartdata = []
    for i in (
        response.get("data", {})
        .get("attributes", {})
        .get("ohlcv_list", [])[::-1]
    ):
        date = datetime.fromtimestamp(float(int(i[0])))
        labels.append(date.strftime("%d/%m/%y %H:%M"))
        chartdata.append(float(i[1]))
    data = {
        "labels": labels,
        "chartdata": chartdata,
    }
    return JsonResponse(data)


def calculate_coin_amount(request):
    from_token = request.GET.get("from")
    to_token = request.GET.get("to")
    amount = float(request.GET.get("amount", 0))
    calc_amount = 0
    if all((from_token, to_token, amount)):
        from_token_price = get_token_price(from_token)
        to_token_price = get_token_price(to_token)
        calc_amount = round(((from_token_price * amount) / to_token_price), 3)
    swap_url = generate_swap_url(from_token, to_token, amount)
    return JsonResponse({"amount": calc_amount, "swap_url": swap_url})


@require_POST
@csrf_exempt
def complate_transaction(request):
    allowed_from = timezone.now() - timezone.timedelta(minutes=5)
    data = json.loads(request.body.decode("utf-8"))
    stacking = Staking.objects.filter(pk=data.get("stak")).first()
    if not stacking:
        return JsonResponse({"ERROR": "No Staking data"}, status=400)
    first_coin = stacking.first_coin.address
    second_coin = stacking.second_coin.address
    user_wallet = data.get("userWallet")
    stacking_wallet = settings.STAKING_WALLET
    amount = float(data.get("priceing", {}).get("source", 0))
    amount_range = (amount * 0.99, amount * 1.01)
    second_amount = float(data.get("priceing", {}).get("destination", 0))
    second_amount_range = (second_amount * 0.99, second_amount * 1.01)
    with PolygonScan("6DCZN7VF1WJRIMJRHPSKV7Z5TF6X4KESTH", False) as matic:
        first_coin_tx_data = matic.get_erc20_token_transfer_events_by_contract_address_paginated(
            first_coin,
            1,
            100,
            "desc",
        )
        second_coin_tx_data = matic.get_erc20_token_transfer_events_by_contract_address_paginated(
            second_coin,
            1,
            100,
            "desc",
        )
    first_data = None
    second_data = None
    for item in first_coin_tx_data:
        date = timezone.make_aware(
            datetime.fromtimestamp(int(item["timeStamp"]))
        )
        if date > allowed_from:
            if all(
                (
                    user_wallet == item["from"],
                    stacking_wallet == item["to"],
                )
            ):
                value = int(item["value"]) / int(item["tokenDecimal"])
                if amount_range[0] < value and value < amount_range[1]:
                    first_data = item["hash"]
                    break
    if not first_data:
        return JsonResponse(
            {
                "ERROR": f"{stacking.first_coin.symbol} Transaction Not found",
            },
            status=400,
        )
    for item in second_coin_tx_data:
        date = timezone.make_aware(
            datetime.fromtimestamp(int(item["timeStamp"]))
        )
        if date > allowed_from:
            if all(
                (
                    user_wallet == item["from"],
                    stacking_wallet == item["to"],
                )
            ):
                value = int(item["value"]) / int(item["tokenDecimal"])
                if (
                    second_amount_range[0] < value
                    and value < second_amount_range[1]
                ):
                    second_data = item["hash"]
                    break
    if not second_data:
        return JsonResponse(
            {
                "ERROR": f"{stacking.second_coin.symbol} Transaction Not found",
            },
            status=400,
        )
    passcode = generate_passcode(user_wallet)
    UserStaking.objects.create(
        tx_hash=first_data,
        second_tx_hash=second_data,
        passcode=passcode,
        from_address=user_wallet,
        to_address=stacking_wallet,
        amount_base=amount,
        amount_quote=second_amount,
        apr=stacking.apr,
        staking=stacking,
        staking_data=json.dumps(stacking.get_data_json()),
    )
    return JsonResponse(
        {
            "passcode": passcode,
        },
        status=200,
    )


@require_POST
@csrf_exempt
def check_contract(request):
    address = request.POST.get("address")
    passcode = request.POST.get("passcode")
    return JsonResponse(
        UserStaking.get_stak_data_by_passcode(address, passcode), safe=False
    )
