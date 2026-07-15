from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "lead", "contract", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("lead__first_name", "lead__last_name", "lead__phone", "lead__email")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Основная информация", {"fields": ("lead", "contract", "is_active")}),
        ("Системные поля", {"fields": ("created_at", "updated_at"), "classes": ("collapse",)}),
    )
