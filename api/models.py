from django.db import models
from django.utils import timezone
from utils.exchange import get_token_price

import json


class Token(models.Model):
    name = models.CharField("Անվանում", max_length=250)
    symbol = models.CharField("Սիմվոլ", max_length=250)
    address = models.CharField("Հասցե", max_length=250, unique=True)
    image_url = models.CharField("Նկարի հղում", max_length=250)
    decimals = models.PositiveSmallIntegerField("Decimals")
    allow_to_buy_dench = models.BooleanField(
        "Թույլատրել գնել DENCH", default=True
    )

    @classmethod
    def get_address_by_pk(cls, pk):
        if pk == "DENCH":
            return "0x2dec733c58388516a1C0E97BBb373dbE906D2797"
        return getattr(cls.objects.filter(pk=pk).first(), "address", None)

    def get_data_json(self):
        return {
            "id": self.pk,
            "name": self.name,
            "symbol": self.symbol,
            "image_url": self.image_url,
        }

    def get_full_data_json(self):
        data = self.get_data_json()
        data["price"] = get_token_price(self.pk)
        return data

    @classmethod
    def get_matic_symbols_for_buy(cls):
        return [
            item.get_data_json()
            for item in cls.objects.filter(allow_to_buy_dench=True)
        ]

    def __str__(self):
        return f"{self.name} ({self.symbol})"

    class Meta:
        verbose_name = "տոկեն"
        verbose_name_plural = "Տոկեններ"


class Staking(models.Model):
    first_coin = models.ForeignKey(
        Token,
        on_delete=models.CASCADE,
        verbose_name="Առաջին Տոկեն",
        related_name="as_first",
    )
    second_coin = models.ForeignKey(
        Token,
        on_delete=models.CASCADE,
        verbose_name="Երկրորդ Տոկեն",
        related_name="as_second",
    )
    apr = models.PositiveSmallIntegerField(
        "Տարեկան շահութաբերություն (APR) %", default=0
    )

    def get_data_json(self):
        return {
            "id": self.pk,
            "source": self.first_coin.get_full_data_json(),
            "destination": self.second_coin.get_full_data_json(),
            "apr": self.apr,
        }

    @classmethod
    def get_staking_data(cls):
        return [item.get_data_json() for item in cls.objects.all()]

    def __str__(self):
        return f"{self.first_coin} - {self.second_coin} (APR: {self.apr}%)"

    class Meta:
        verbose_name = "զույգ"
        verbose_name_plural = "Սթեքինգ"


class UserStaking(models.Model):
    tx_hash = models.CharField("Առաջին Փոխանցման հեշ", max_length=200)
    second_tx_hash = models.CharField("Երկրորդ Փոխանցման հեշ", max_length=200)
    passcode = models.CharField("Գաղտնաբառ", max_length=200)
    from_address = models.CharField("Փոխանցող", max_length=200)
    to_address = models.CharField("Ստացող", max_length=200)
    amount_base = models.PositiveIntegerField("Առաջին տոկենի քանակ")
    amount_quote = models.PositiveIntegerField("Երկրորդ տոկենի քանակ")
    apr = models.PositiveSmallIntegerField("Տարեկան շահութաբերություն (APR) %")
    staking = models.ForeignKey(
        Staking,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_stakings",
        verbose_name="Սթեքինգ",
    )
    staking_data = models.TextField("Ինֆորմացիա Սթեքինգի մասին")
    created_at = models.DateTimeField("Ավելացված է՝", auto_now_add=True)
    is_active = models.BooleanField("Ակտիվ է", default=True)

    def get_staking_data(self):
        return json.loads(self.staking_data)

    @property
    def first_coin(self):
        return self.get_staking_data()["source"]

    @property
    def second_coin(self):
        return self.get_staking_data()["destination"]

    @property
    def days_left(self):
        return (timezone.now() - self.created_at).days

    @property
    def dayly_profit(self):
        return round((self.amount_quote * (self.apr / 100)) / 365.5, 2)

    def get_data_json(self):
        return {
            "id": self.pk,
            "amount_base": self.amount_base,
            "amount_quote": self.amount_quote,
            "first_coin": self.first_coin,
            "second_coin": self.second_coin,
            "apr": self.apr,
            "staking_data": self.get_staking_data(),
            "created_at": self.created_at.strftime("%d/%m/%Y %H:%m"),
            "profit": self.dayly_profit * self.days_left,
        }

    @classmethod
    def get_stak_data_by_passcode(cls, address, passcode):
        return [
            item.get_data_json()
            for item in cls.objects.filter(
                from_address=address, passcode=passcode, is_active=True
            )
        ]

    @classmethod
    def return_passcode(cls, address):
        if address:
            return getattr(
                cls.objects.filter(from_address=address).first(),
                "passcode",
                None,
            )

    def __str__(self):
        return self.staking

    class Meta:
        verbose_name = "սթեք"
        verbose_name_plural = "Կատարված Սթեքինգ"
