from django.db import models
from django.urls import reverse

from contracts.models import Contract
from leads.models import Lead


class Customer(models.Model):
    """Модель активного клиента"""

    lead: models.OneToOneField = models.OneToOneField(
        Lead,
        on_delete=models.CASCADE,
        verbose_name="Потенциальный клиент",
        related_name="customer",
        help_text="Выберите потенциального клиента для перевода в активные",
        db_index=True,
    )
    contract: models.OneToOneField = models.OneToOneField(
        Contract,
        on_delete=models.CASCADE,
        verbose_name="Контракт",
        related_name="customer",
        help_text="Выберите контракт для клиента",
        db_index=True,
    )
    is_active: models.BooleanField = models.BooleanField(default=True, verbose_name="Активен", db_index=True)
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания", db_index=True
    )
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Активный клиент"
        verbose_name_plural = "Активные клиенты"
        ordering = ["-created_at"]
        permissions = [
            ("can_view_customer", "Может просматривать активных клиентов"),
            ("can_create_customer", "Может создавать активных клиентов"),
            ("can_edit_customer", "Может редактировать активных клиентов"),
            ("can_delete_customer", "Может удалять активных клиентов"),
        ]
        indexes = [
            models.Index(fields=["lead"]),
            models.Index(fields=["contract"]),
            models.Index(fields=["is_active", "created_at"]),
        ]

    def __str__(self):
        return f"{self.lead.get_full_name()}"

    def get_absolute_url(self):
        return reverse("customers:detail", kwargs={"pk": self.pk})

    def get_full_name(self):
        return self.lead.get_full_name()
