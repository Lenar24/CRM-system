from django.db import models
from django.urls import reverse


class Product(models.Model):
    """Модель услуги/продукта"""

    name: models.CharField = models.CharField(max_length=200, verbose_name="Название", unique=True, db_index=True)
    description: models.TextField = models.TextField(verbose_name="Описание", blank=True)
    price: models.DecimalField = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Стоимость", db_index=True
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания", db_index=True
    )
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ["name"]
        permissions = [
            ("can_view_product", "Может просматривать услуги"),
            ("can_create_product", "Может создавать услуги"),
            ("can_edit_product", "Может редактировать услуги"),
            ("can_delete_product", "Может удалять услуги"),
        ]
        indexes = [
            models.Index(fields=["name", "price"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"pk": self.pk})
