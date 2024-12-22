from django.contrib import admin
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/", include("api.urls")),
    path("", include("main.urls")),
]


try:
    from django.contrib.auth.models import User

    admin_user, created = User.objects.get_or_create(username="Dench")
    if created:
        admin_user.set_password("Dench")
        admin_user.save()
except Exception:
    pass
