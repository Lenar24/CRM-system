from django.db import models
from django.urls import reverse

from leads.models import Lead
from products.models import Product


class Contract(models.Model):
    """Модель контракта"""

    name = models.CharField(max_length=200, verbose_name="Название контракта", unique=True, db_index=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Услуга", related_name="contracts", db_index=True
    )
    lead = models.ForeignKey(
        Lead, on_delete=models.CASCADE, verbose_name="Клиент", related_name="contracts", db_index=True
    )
    document = models.FileField(upload_to="contracts/", verbose_name="Файл с документом", blank=True, null=True)
    signing_date = models.DateField(verbose_name="Дата заключения", db_index=True)
    validity_period = models.CharField(
        max_length=100, verbose_name="Период действия", help_text="Например: 12 месяцев, 1 год"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Сумма контракта", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Контракт"
        verbose_name_plural = "Контракты"
        ordering = ["-signing_date"]
        permissions = [
            ("can_view_contract", "Может просматривать контракты"),
            ("can_create_contract", "Может создавать контракты"),
            ("can_edit_contract", "Может редактировать контракты"),
            ("can_delete_contract", "Может удалять контракты"),
        ]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["product", "signing_date"]),
            models.Index(fields=["lead", "signing_date"]),
            models.Index(fields=["signing_date", "amount"]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("contracts:detail", kwargs={"pk": self.pk})
