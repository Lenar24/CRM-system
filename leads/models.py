from django.db import models
from django.urls import reverse

from ads.models import AdCampaign


class Lead(models.Model):
    """Модель потенциального клиента"""

    first_name = models.CharField(max_length=100, verbose_name="Имя", db_index=True)
    last_name = models.CharField(max_length=100, verbose_name="Фамилия", db_index=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", db_index=True)
    email = models.EmailField(verbose_name="Email", db_index=True)
    campaign = models.ForeignKey(
        AdCampaign,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Рекламная кампания",
        related_name="leads",
        db_index=True,
    )
    is_converted = models.BooleanField(default=False, verbose_name="Переведен в активного", db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания", db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Потенциальный клиент"
        verbose_name_plural = "Потенциальные клиенты"
        ordering = ["-created_at"]
        permissions = [
            ("can_view_lead", "Может просматривать потенциальных клиентов"),
            ("can_create_lead", "Может создавать потенциальных клиентов"),
            ("can_edit_lead", "Может редактировать потенциальных клиентов"),
            ("can_delete_lead", "Может удалять потенциальных клиентов"),
            ("can_convert_lead", "Может переводить потенциальных клиентов в активных"),
        ]
        indexes = [
            models.Index(fields=["last_name", "first_name"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["email"]),
            models.Index(fields=["campaign", "is_converted"]),
        ]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_absolute_url(self):
        return reverse("leads:detail", kwargs={"pk": self.pk})

    def get_full_name(self):
        return f"{self.last_name} {self.first_name}"
