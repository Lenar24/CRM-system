from django.contrib import admin

from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "phone", "email", "campaign", "is_converted", "created_at")
    list_filter = ("is_converted", "campaign", "created_at")
    search_fields = ("last_name", "first_name", "phone", "email")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Основная информация", {"fields": ("first_name", "last_name", "phone", "email", "campaign")}),
        ("Статус", {"fields": ("is_converted",)}),
        ("Системные поля", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
