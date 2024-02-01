from django.urls import path,include
from django.contrib.auth.decorators import login_required
from .views import (index, login, register, logout, whitepaper, whitepaper_pdf, privacy, register, activate, shop,
                    partners, ChartData, CoinTransactionView, FinalTransaction, FinalPairedTransaction,
                    ContractInfoCollector, ResignContract)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', index, name='index'),
    path('login/', login, name='login'),
    # path('calculate/', calculation, name='calculation'),
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    # path('reset/', reset, name='reset'),
    # path('password-reset-confirm/<uidb64>/<token>/', reset_confirm, name='password_reset_confirm'),
    # path('reset-activate/<uidb64>/<token>/', reset_activate, name="reset_activate"),
    path('logout/', login_required(logout), name='logout'),
    path('shop/', login_required(shop), name='shop'),
    path('privacy/', privacy, name='privacy'),
    path('partners/', partners, name='partners'),
    path('whitepaper/', whitepaper, name='whitepaper'),
    path('whitepaper/pdf/', whitepaper_pdf, name='whitepaper_pdf'),
    path('my-account/', include('main.urls_my_account')),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('api/chart', ChartData.as_view()),
    path('api/calculate_coin_amount', CoinTransactionView.as_view()),
    path('api/transaction', FinalTransaction.as_view()),
    path('api/paired_transaction', FinalPairedTransaction.as_view()),
    path('api/check_contract', ContractInfoCollector.as_view()),
    path('api/resign_contract', ResignContract.as_view())
]

