from django.shortcuts import render, redirect
from django.http import FileResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings as django_settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from utils.tokenGenerator import account_activation_token
from .DBTableManager import TableManager
from .forms import SignUpForm
from .models import User
from django.views.generic.edit import FormView

import os
from datetime import datetime

from coinpaprika import client as cp

from rest_framework.views import APIView
from rest_framework.response import Response

from .CoinInfoCollector import CoinInfoCollector
from .MetamaskManager import MetamaskManager


# from .RedisControl import RedisControl

def _get_price(to_coin="USD"):
    return MetamaskManager.get_price(to_coin)


def _get_price_usd(coin):
    return MetamaskManager.get_price_usd(coin)


def index(request):
    args = {'price': 10.353}
    return render(request, 'index.html', args)


def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'registration/login.html')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(request.POST)
        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                return render(request, 'registration/login.html',
                              {'errors': 'Please, activate your account.', 'form_email': email})
            user = authenticate(email=user.email, password=password)
            print('user1', user)
        except Exception as e:
            print(e)
            user = None
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'registration/login.html',
                          {'errors': 'Invalid email or password.', 'form_email': email})


def logout(request):
    auth_logout(request)
    return redirect('index')


def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return render(request, 'registration/register.html')
    if request.method == 'POST':
        print('request.POST', request.POST)
        form = SignUpForm(request.POST)
        print('form.errors', form.errors)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            # user.language = get_language_from_request(request, check_path=False)
            user.save()
            mail_subject = 'Activate your account.'
            message = render_to_string('registration/registration_email.html', {
                'user': user,
                'url': request.get_full_path(),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'domain': get_current_site(request).domain,
                'protocol': 'http',
            })
            to_email = form.cleaned_data.get('email')
            print('message', message)
            send_mail(mail_subject, '', django_settings.EMAIL_HOST_USER, [to_email], html_message=message)
            final_form = {'form': form,
                          'success': 'In order to complete your registration you need to confirm your email address.'}
            return render(request, 'registration/register.html', final_form)
        else:
            print(form)
            return render(request, 'registration/register.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        return render(request, 'registration/res_activate.html', {'activate': True})
    else:
        return render(request, 'registration/res_activate.html', {'activate': False})


def shop(request):
    return render(request, 'shop.html')


def privacy(request):
    return render(request, 'privacy.html')


def partners(request):
    return render(request, 'partners.html')


def whitepaper(request):
    return render(request, 'whitepaper.html')


def whitepaper_pdf(request):
    return FileResponse(open(os.path.join(django_settings.BASE_DIR, 'templates/whitepaper.pdf'), 'rb'))


def handler404(request, exception):
    print('error:', exception)
    return render(request, 'error404.html')


class ChartData(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        labels = []
        chartdata = []
        post_data = request.data
        # control = RedisControl(host="localhost", sql_db=settings.DATABASES['default']['NAME'])
        coin_control = CoinInfoCollector("dench-denchcoin", django_settings.DATABASES['default']['NAME'])
        info_for_chart = coin_control.get_candle(post_data["type"])
        for info in info_for_chart:
            date = datetime.fromtimestamp(float(int(info[0])))
            labels.append(date.strftime('%d/%m/%y %H:%M'))
            chartdata.append(float(info[1]))

        # info_for_chart, info_date_for_chart = control.get_ticker(post_data["type"])
        # for ind in range(len(info_for_chart)):
        #     labels.append(datetime.fromtimestamp(float(int(info_date_for_chart[ind]))))
        #     chartdata.append(float(info_for_chart[ind]))
        data = {
            "labels": labels,
            "chartdata": chartdata,
        }
        return Response(data)


# def calculation(self, denchcoin_type):
#     self.denchcoin_type = denchcoin_type
#     choice_for_exchange = []
#     if Calculator.denchcoin_type == "BEP-20":
#         choice_for_exchange += [('BUSD', 'BUSD'), ('BNB', 'BNB')]
#     else:
#         choice_for_exchange += [('USDT', 'USDT'), ('ETH', 'ETH'), ('BTC', 'BTC')]
#     Calculator.update_chois(tuple(choice_for_exchange))


class CoinTransactionView(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        data = request.data
        base_price_usd = _get_price_usd(data["from"])
        quote_price_usd = _get_price_usd(data["to"])
        calc_amount = round(base_price_usd * float(data["amount"]) / quote_price_usd, 3)
        new_data = {
            "amount": calc_amount,
        }
        return Response(new_data)


class FinalTransaction(APIView):
    authentication_classes = []
    permission_classes = []
    address = "0xa1e453b2c576acEEA6d406b7366536feB8A6DF55"
    private_key = "34dfb81837d00d9b5992d911caaeeda19a76015ef74ad88d018f7badbae1e3e4"
    metaMask = MetamaskManager(address, private_key)

    def post(self, request):
        data = request.data
        called_params = {
            'price': _get_price(data['expected_coin']),
            'coin_amount': data['coin_amount'],
            'expected_coin': data['expected_coin'],
            'chain_type': data['chain_type'],
        }
        response = self.metaMask.catching_loop_of_transaction(called_params)
        new_data = {
            "response": response,
        }
        return Response(new_data)


class FinalPairedTransaction(APIView):
    authentication_classes = []
    permission_classes = []
    address = "0xa1e453b2c576acEEA6d406b7366536feB8A6DF55"
    private_key = "34dfb81837d00d9b5992d911caaeeda19a76015ef74ad88d018f7badbae1e3e4"
    metaMask = MetamaskManager(address, private_key)

    def post(self, request):
        data = request.data
        called_params = {
            'base': data['base'],
            'base_amount': data['base_amount'],
            'quote': data['quote'],
            'quote_amount': data['quote_amount'],
            'apr': data['apr'],
            'price': _get_price(data['quote']),
            'chain_type': data['chain_type']
        }
        response = self.metaMask.catching_loop_of_paired_transaction(called_params)
        new_data = {
            "response": response,
        }
        return Response(new_data)


class ContractInfoCollector(APIView):
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def post(request):
        data = request.data
        table = TableManager("paired_transactions_final", django_settings.DATABASES['default']['NAME'])
        labels, pairs = table.get_pairs(wallet_address=data['wallet_address'], passcode=data['passcode'])
        if pairs:
            for i in range(len(pairs)):
                pairs[i][-1] = int(datetime.strptime(pairs[i][-1], '%Y-%m-%d %H:%M:%S.%f').timestamp() * 1000)

        data = {
            "labels": labels,
            "pairs": pairs,
        }
        return Response(data)


class ResignContract(APIView):
    authentication_classes = []
    permission_classes = []
    address = "0xa1e453b2c576acEEA6d406b7366536feB8A6DF55"
    private_key = "34dfb81837d00d9b5992d911caaeeda19a76015ef74ad88d018f7badbae1e3e4"
    metaMask = MetamaskManager(address, private_key)

    def post(self, request):
        data = request.data
        called_params = {
            'wallet_address': data['wallet_address'],
            'passcode': data['passcode'],
            'index': data['index'],
            'expected_coin': 'TokenLP',
        }
        response = self.metaMask.catching_loop_of_resign_contract(called_params)
        new_data = {
            "response": response,
        }
        return Response(new_data)
