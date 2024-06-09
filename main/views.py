from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import Whitepaper, Partner, Subscribe, RoadMap
from api.models import Token, Staking

import json


def index(request):
    return render(
        request,
        "main/index.html",
        {
            "is_index": True,
            "RoadMap": RoadMap.objects.all(),
            "MATIC": json.dumps(Token.get_matic_symbols_for_buy()),
            "Staking": json.dumps(Staking.get_staking_data()),
            "STAKING_WALLET": settings.STAKING_WALLET,
        },
    )


def whitepaper(request):
    return render(
        request,
        "main/whitepaper.html",
        {"Whitepaper": Whitepaper.objects.all()},
    )


def partner(request):
    return render(
        request,
        "main/partner.html",
        {"Partner": Partner.objects.all()},
    )


@require_POST
def subscribe(request):
    email = request.POST.get("email")
    if email:
        Subscribe.objects.create(email=email)
        return HttpResponseRedirect(reverse("index"))
    return HttpResponseBadRequest()
