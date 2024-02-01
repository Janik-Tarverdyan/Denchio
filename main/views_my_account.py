from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.forms import PasswordChangeForm


def dashboard(request):
    return render(request,'my-account/dashboard.html')


def orders(request):
    return render(request,'my-account/orders.html')


def address(request):
    return render(request,'my-account/address.html')


def billing(request):
    if request.method == 'GET':
        return render(request,'my-account/billing.html')


def account_details(request):
    if request.method == 'GET':
        return render(request,'my-account/account-details.html')


def change_password(request):
    if request.method == 'GET':
        return render(request,'registration/password_change_form.html')
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            return render(request,'registration/password_change_done.html')
        else:
            print(form)
            return render(request,'registration/password_change_form.html', {'form':form})
