from django.core.validators import EmailValidator
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from ads.models import AdCampaign
from CRM_system.validators import validate_full_name


class Lead(models.Model):
    """Модель потенциального клиента"""

    first_name: models.CharField = models.CharField(
        max_length=100, verbose_name="Имя", db_index=True, validators=[validate_full_name]
    )
    last_name: models.CharField = models.CharField(
        max_length=100, verbose_name="Фамилия", db_index=True, validators=[validate_full_name]
    )
    phone: PhoneNumberField = PhoneNumberField(verbose_name="Телефон", db_index=True, region="RU")
    email: models.EmailField = models.EmailField(
        verbose_name="Email", db_index=True, validators=[EmailValidator(message="Введите корректный email адрес")]
    )
    campaign: models.ForeignKey = models.ForeignKey(
        AdCampaign,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Рекламная кампания",
        related_name="leads",
        db_index=True,
    )
    is_converted: models.BooleanField = models.BooleanField(
        default=False, verbose_name="Переведен в активного клиента", db_index=True
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания", db_index=True
    )
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

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
