from django.contrib import admin

from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("name", "product", "lead", "signing_date", "amount", "created_at")
    list_filter = ("signing_date", "product", "created_at")
    search_fields = ("name", "lead__first_name", "lead__last_name", "product__name")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "signing_date"

    fieldsets = (
        ("Основная информация", {"fields": ("name", "product", "lead", "document")}),
        ("Детали контракта", {"fields": ("signing_date", "validity_period", "amount")}),
        ("Системные поля", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
