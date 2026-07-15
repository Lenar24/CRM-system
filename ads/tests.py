from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from products.models import Product

from .models import AdCampaign


class AdCampaignModelTest(TestCase):
    """Тесты для модели AdCampaign"""

    def setUp(self):
        self.product = Product.objects.create(name="Тестовая услуга", description="Описание", price=1000.00)
        self.campaign = AdCampaign.objects.create(
            name="Тестовая кампания", product=self.product, channel="social", budget=5000.00, is_active=True
        )

    def test_campaign_creation(self):
        """Проверка создания кампании"""
        self.assertEqual(self.campaign.name, "Тестовая кампания")
        self.assertEqual(self.campaign.product, self.product)
        self.assertEqual(self.campaign.budget, 5000.00)
        self.assertTrue(self.campaign.is_active)

    def test_campaign_str(self):
        """Проверка строкового представления"""
        self.assertEqual(str(self.campaign), "Тестовая кампания")

    def test_get_absolute_url(self):
        """Проверка URL для детальной страницы"""
        self.assertEqual(self.campaign.get_absolute_url(), reverse("ads:detail", kwargs={"pk": self.campaign.pk}))


class AdCampaignViewsTest(TestCase):
    """Тесты для представлений AdCampaign"""

    def setUp(self):
        # Создаем пользователя с правами
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        # Добавляем разрешения
        permissions = Permission.objects.filter(
            codename__in=[
                "can_view_adcampaign",
                "can_create_adcampaign",
                "can_edit_adcampaign",
                "can_delete_adcampaign",
            ]
        )
        self.user.user_permissions.add(*permissions)
        self.client.login(username="testuser", password="testpass123")

        # Создаем тестовую услугу
        self.product = Product.objects.create(name="Тестовая услуга", description="Описание", price=1000.00)

        # Создаем тестовую кампанию
        self.campaign = AdCampaign.objects.create(
            name="Тестовая кампания", product=self.product, channel="social", budget=5000.00, is_active=True
        )

    def test_campaign_list_view(self):
        response = self.client.get(reverse("ads:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ads/ads-list.html")
        # Проверяем, что в контексте есть переменная 'ads'
        self.assertIn("ads", response.context)
        # Проверяем, что кампания отображается
        self.assertContains(response, "Тестовая кампания")

    def test_campaign_detail_view(self):
        """Проверка детальной страницы кампании"""
        response = self.client.get(reverse("ads:detail", kwargs={"pk": self.campaign.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ads/ads-detail.html")
        self.assertContains(response, "Тестовая кампания")

    def test_campaign_create_view(self):
        """Проверка создания кампании"""
        response = self.client.post(
            reverse("ads:create"),
            {
                "name": "Новая кампания",
                "product": self.product.pk,
                "channel": "context",
                "budget": 10000.00,
                "is_active": True,
            },
        )
        self.assertEqual(response.status_code, 302)  # Редирект после создания
        self.assertEqual(AdCampaign.objects.count(), 2)
        self.assertTrue(AdCampaign.objects.filter(name="Новая кампания").exists())

    def test_campaign_update_view(self):
        """Проверка редактирования кампании"""
        response = self.client.post(
            reverse("ads:edit", kwargs={"pk": self.campaign.pk}),
            {
                "name": "Обновленная кампания",
                "product": self.product.pk,
                "channel": "email",
                "budget": 15000.00,
                "is_active": False,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.campaign.refresh_from_db()
        self.assertEqual(self.campaign.name, "Обновленная кампания")
        self.assertEqual(self.campaign.channel, "email")
        self.assertEqual(self.campaign.budget, 15000.00)
        self.assertFalse(self.campaign.is_active)

    def test_campaign_delete_view(self):
        """Проверка удаления кампании"""
        response = self.client.post(reverse("ads:delete", kwargs={"pk": self.campaign.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(AdCampaign.objects.count(), 0)


class AdCampaignPermissionsTest(TestCase):
    """Тесты прав доступа"""

    def setUp(self):
        self.product = Product.objects.create(name="Тестовая услуга", description="Описание", price=1000.00)
        self.campaign = AdCampaign.objects.create(
            name="Тестовая кампания", product=self.product, channel="social", budget=5000.00
        )

    def test_user_without_permissions(self):
        """Пользователь без прав не должен видеть кампании"""
        User.objects.create_user(username="nopermission", password="testpass123")
        self.client.login(username="nopermission", password="testpass123")

        response = self.client.get(reverse("ads:list"))
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_user_with_permissions(self):
        user = User.objects.create_user(username="withpermission", password="testpass123")
        permission = Permission.objects.get(codename="can_view_adcampaign")
        user.user_permissions.add(permission)
        self.client.login(username="withpermission", password="testpass123")

        response = self.client.get(reverse("ads:list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("ads", response.context)
        self.assertContains(response, "Тестовая кампания")

    def test_unauthenticated_user(self):
        """Неавторизованный пользователь должен быть перенаправлен на логин"""
        response = self.client.get(reverse("ads:list"))
        self.assertEqual(response.status_code, 302)  # Редирект на логин
        self.assertIn("/login/", response.url)
