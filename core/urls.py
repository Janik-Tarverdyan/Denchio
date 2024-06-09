from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/", include("api.urls")),
    path("", include("main.urls")),
]
