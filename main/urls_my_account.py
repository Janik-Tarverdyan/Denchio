from django.urls import path,include
from django.contrib.auth.decorators import login_required
from .views_my_account import (dashboard, orders, address, account_details, billing, change_password)



urlpatterns = [
    path('dashboard/', login_required(dashboard), name="dashboard"),
    path('orders/', login_required(orders), name="orders"),
    path('address/', login_required(address), name="address"),
    path('address/billing', login_required(billing), name="billing"),
    path('account-details/', login_required(account_details), name="account_details"),
    path('change-password/', login_required(change_password), name="change_password"),
]

