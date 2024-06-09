from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Token, Staking
from .forms import TokenCreationForm


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = (
        "image",
        "name",
        "symbol",
        "decimals",
        "allow_to_buy_dench",
    )
    list_display_links = list_display

    def image(self, obj=None):
        return mark_safe(f'<img src="{obj.image_url}">')

    image.short_description = "Նկար"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return (
                "name",
                "symbol",
                "address",
                "image_url",
                "decimals",
                "image",
            )
        return super().get_readonly_fields(request, obj)

    def save_model(self, request, obj, form, change) -> None:
        if not change:
            obj.name = form.data["name"]
            obj.symbol = form.data["symbol"]
            obj.image_url = form.data["image_url"]
            obj.decimals = form.data["decimals"]
        return super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, change=False, **kwargs):
        if not obj:
            return TokenCreationForm
        return super().get_form(request, obj, change, **kwargs)


@admin.register(Staking)
class StakingAdmin(admin.ModelAdmin):
    list_display = ("first_coin", "second_coin", "apr")
    list_display_links = list_display
