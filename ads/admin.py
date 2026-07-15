from django.contrib import admin

from .models import AdCampaign


@admin.register(AdCampaign)
class AdCampaignAdmin(admin.ModelAdmin):
    list_display = ("name", "product", "channel", "budget", "is_active", "created_at")
    list_filter = ("channel", "is_active", "created_at")
    search_fields = ("name", "product__name")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Основная информация", {"fields": ("name", "product", "channel", "budget", "is_active")}),
        ("Системные поля", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
