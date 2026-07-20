from django.db import models
from django.urls import reverse

from products.models import Product


class AdCampaign(models.Model):
    """Модель рекламной кампании"""

    CHANNEL_CHOICES = [
        # 📱 Социальные сети
        ("social_vk", "ВКонтакте (VK)"),
        ("social_tg", "Telegram"),
        ("social_ok", "Одноклассники"),
        ("social_fb", "Facebook"),
        ("social_inst", "Instagram"),
        ("social_youtube", "YouTube"),
        ("social_tiktok", "TikTok"),
        ("social_dzen", "Дзен"),
        # 🔍 Поисковые системы
        ("seo_yandex", "Яндекс SEO"),
        ("seo_google", "Google SEO"),
        ("context_yandex", "Яндекс.Директ"),
        ("context_google", "Google Ads"),
        # 📧 Email-маркетинг
        ("email_newsletter", "Email-рассылка"),
        ("email_autoresponder", "Авто-рассылка"),
        # 📢 Медийная реклама
        ("media_banner", "Баннерная реклама"),
        ("media_video", "Видеореклама"),
        ("media_native", "Нативная реклама"),
        # 🤝 Партнёрские программы
        ("partner_affiliate", "Партнёрская программа"),
        ("partner_influencer", "Инфлюенс-маркетинг"),
        # 📡 Офлайн-каналы
        ("offline_radio", "Радио"),
        ("offline_tv", "Телевидение"),
        ("offline_print", "Печатная реклама"),
        ("offline_outdoor", "Наружная реклама"),
        ("offline_event", "Мероприятия"),
        # 🎯 Другие
        ("other", "Другое"),
    ]

    name: models.CharField = models.CharField(
        max_length=200,
        verbose_name="Название кампании",
        unique=True,
        help_text="Введите название рекламной кампании",
        db_index=True,
    )
    product: models.ForeignKey = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Рекламируемая услуга", related_name="campaigns", db_index=True
    )
    channel: models.CharField = models.CharField(
        max_length=20, choices=CHANNEL_CHOICES, verbose_name="Канал продвижения", default="social"
    )
    budget: models.DecimalField = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Бюджет на рекламу",
        help_text="Укажите бюджет в рублях",
        db_index=True,
    )
    is_active: models.BooleanField = models.BooleanField(default=True, verbose_name="Активна", db_index=True)
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания", db_index=True
    )
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Рекламная кампания"
        verbose_name_plural = "Рекламные кампании"
        ordering = ["-created_at"]
        permissions = [
            ("can_view_adcampaign", "Может просматривать рекламные кампании"),
            ("can_create_adcampaign", "Может создавать рекламные кампании"),
            ("can_edit_adcampaign", "Может редактировать рекламные кампании"),
            ("can_delete_adcampaign", "Может удалять рекламные кампании"),
        ]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["product", "created_at"]),
            models.Index(fields=["is_active", "created_at"]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ads:detail", kwargs={"pk": self.pk})
