from django.urls import path
from . import views


urlpatterns = [
    path("chart", views.get_chart, name="get_chart"),
    path("price", views.get_price, name="get_price"),
    path("check_contract", views.check_contract, name="check_contract"),
    path(
        "calculate_coin_amount",
        views.calculate_coin_amount,
        name="calculate_coin_amount",
    ),
    path(
        "complate_transaction",
        views.complate_transaction,
        name="complate_transaction",
    ),
]
