from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from ads.models import AdCampaign
from products.models import Product

from .models import Lead


class LeadModelTest(TestCase):
    def setUp(self):
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

    def test_lead_creation(self):
        self.assertEqual(self.lead.first_name, "Иван")
        self.assertEqual(self.lead.last_name, "Петров")
        self.assertEqual(str(self.lead), "Петров Иван")

    def test_get_full_name(self):
        self.assertEqual(self.lead.get_full_name(), "Петров Иван")


class LeadViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        permissions = Permission.objects.filter(
            codename__in=["can_view_lead", "can_create_lead", "can_edit_lead", "can_delete_lead", "can_convert_lead"]
        )
        self.user.user_permissions.add(*permissions)
        self.client.login(username="testuser", password="testpass123")

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

    def test_lead_list_view(self):
        response = self.client.get(reverse("leads:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "leads/leads-list.html")
        self.assertContains(response, "Петров Иван")

    def test_lead_detail_view(self):
        response = self.client.get(reverse("leads:detail", kwargs={"pk": self.lead.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "leads/leads-detail.html")

    def test_lead_create_view(self):
        response = self.client.post(
            reverse("leads:create"),
            {
                "first_name": "Петр",
                "last_name": "Сидоров",
                "phone": "+7 888 123-45-67",
                "email": "petr@example.com",
                "campaign": self.campaign.pk,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Lead.objects.count(), 2)

    def test_lead_delete_view(self):
        response = self.client.post(reverse("leads:delete", kwargs={"pk": self.lead.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Lead.objects.count(), 0)
