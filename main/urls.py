from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("whitepaper/", views.whitepaper, name="whitepaper"),
    path("partner/", views.partner, name="partner"),
    path("subscribe/", views.subscribe, name="subscribe"),
]
