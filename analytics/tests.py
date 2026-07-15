from datetime import date

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from ads.models import AdCampaign
from contracts.models import Contract
from customers.models import Customer
from leads.models import Lead
from products.models import Product


class AnalyticsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        permission = Permission.objects.get(codename="can_view_adcampaign")
        self.user.user_permissions.add(permission)
        self.client.login(username="testuser", password="testpass123")

        # Создаем тестовые данные
        self.product = Product.objects.create(name="Тестовая услуга", description="Описание", price=1000.00)
        self.campaign = AdCampaign.objects.create(
            name="Тестовая кампания", product=self.product, channel="social", budget=5000.00
        )
        self.lead = Lead.objects.create(
            first_name="Иван",
            last_name="Петров",
            phone="+7 999 123-45-67",
            email="ivan@example.com",
            campaign=self.campaign,
        )
        self.contract = Contract.objects.create(
            name="Тестовый контракт",
            product=self.product,
            lead=self.lead,
            signing_date=date(2026, 1, 15),
            validity_period="12 месяцев",
            amount=100000.00,
        )
        self.customer = Customer.objects.create(lead=self.lead, contract=self.contract, is_active=True)

    def test_statistic_view(self):
        """Проверка страницы статистики"""
        response = self.client.get(reverse("analytics:statistic"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "ads/ads-statistic.html")

    def test_statistic_context(self):
        """Проверка контекста статистики"""
        response = self.client.get(reverse("analytics:statistic"))
        self.assertIn("ads", response.context)
        ads = response.context["ads"]
        self.assertEqual(len(ads), 1)

        ad = ads[0]
        self.assertEqual(ad.name, "Тестовая кампания")
        self.assertEqual(ad.leads_count, 1)
        self.assertEqual(ad.customers_count, 1)
        self.assertEqual(ad.profit, 20.0)  # 100000 / 5000 = 20

    def test_statistic_no_campaigns(self):
        """Проверка статистики без кампаний"""
        AdCampaign.objects.all().delete()
        response = self.client.get(reverse("analytics:statistic"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["ads"]), 0)

    def test_statistic_without_leads(self):
        """Проверка статистики с кампанией без лидов"""
        Lead.objects.all().delete()
        response = self.client.get(reverse("analytics:statistic"))
        self.assertEqual(response.status_code, 200)
        ad = response.context["ads"][0]
        self.assertEqual(ad.leads_count, 0)
        self.assertEqual(ad.customers_count, 0)
        # Проверяем, что profit - это 0 или строка '-'
        self.assertIn(ad.profit, [0, "-"])
