from datetime import date

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from leads.models import Lead
from products.models import Product

from .models import Contract


class ContractModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Тестовая услуга", description="Описание", price=1000.00)
        self.lead = Lead.objects.create(
            first_name="Иван", last_name="Петров", phone="+7 999 123-45-67", email="ivan@example.com"
        )
        self.contract = Contract.objects.create(
            name="Тестовый контракт",
            product=self.product,
            lead=self.lead,
            signing_date=date(2026, 1, 15),
            validity_period="12 месяцев",
            amount=100000.00,
        )

    def test_contract_creation(self):
        self.assertEqual(self.contract.name, "Тестовый контракт")
        self.assertEqual(self.contract.amount, 100000.00)
        self.assertEqual(str(self.contract), "Тестовый контракт")


class ContractViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        permissions = Permission.objects.filter(
            codename__in=["can_view_contract", "can_create_contract", "can_edit_contract", "can_delete_contract"]
        )
        self.user.user_permissions.add(*permissions)
        self.client.login(username="testuser", password="testpass123")

        self.product = Product.objects.create(name="Тестовая услуга", description="Описание", price=1000.00)
        self.lead = Lead.objects.create(
            first_name="Иван", last_name="Петров", phone="+7 999 123-45-67", email="ivan@example.com"
        )
        self.contract = Contract.objects.create(
            name="Тестовый контракт",
            product=self.product,
            lead=self.lead,
            signing_date=date(2026, 1, 15),
            validity_period="12 месяцев",
            amount=100000.00,
        )

    def test_contract_list_view(self):
        response = self.client.get(reverse("contracts:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contracts/contracts-list.html")
        self.assertContains(response, "Тестовый контракт")

    def test_contract_detail_view(self):
        response = self.client.get(reverse("contracts:detail", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "contracts/contracts-detail.html")

    def test_contract_create_view(self):
        response = self.client.post(
            reverse("contracts:create"),
            {
                "name": "Новый контракт",
                "product": self.product.pk,
                "lead": self.lead.pk,
                "signing_date": "2026-02-01",
                "validity_period": "24 месяца",
                "amount": 200000.00,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contract.objects.count(), 2)

    def test_contract_delete_view(self):
        response = self.client.post(reverse("contracts:delete", kwargs={"pk": self.contract.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Contract.objects.count(), 0)
