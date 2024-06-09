from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Whitepaper, Partner, Subscribe, RoadMap


@admin.register(Whitepaper)
class WhitepaperAdmin(admin.ModelAdmin):
    list_display = ("title", "file")
    list_display_links = list_display


@admin.register(RoadMap)
class RoadMapAdmin(admin.ModelAdmin):
    list_display = ("year", "quarter", "description")
    list_display_links = list_display
    list_filter = ("year", "quarter")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "address",
        "phone",
        "website",
    )
    list_display_links = list_display


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        "is_active",
        "email",
        "date_joined",
    )
    list_display_links = list_display[1:]
    readonly_fields = ("send_email", "date_joined")
    exclude = ("email",)
    list_editable = ("is_active",)
    search_fields = ("email",)
    date_hierarchy = "date_joined"

    def send_email(self, obj=None):
        return mark_safe(
            f"""<a href="mailto:{obj.email}">{obj.email}</a>"""
        )
    send_email.short_description = "Էլ․ հասցե"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
