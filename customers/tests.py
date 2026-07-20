from datetime import date

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from contracts.models import Contract
from leads.models import Lead
from products.models import Product

from .models import Customer


class CustomerModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Тестовая услуга", description="Описание", price=1000.00)
        self.lead = Lead.objects.create(
            first_name="Иван",
            last_name="Петров",
            phone="+7 999 123-45-67",
            email="ivan@example.com",
            is_converted=False,
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

    def test_customer_creation(self):
        self.assertEqual(str(self.customer), "Петров Иван")
        self.assertTrue(self.customer.is_active)
        self.assertEqual(self.customer.lead, self.lead)
        self.assertEqual(self.customer.contract, self.contract)

    def test_customer_str(self):
        self.assertEqual(str(self.customer), "Петров Иван")


class CustomerViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        permissions = Permission.objects.filter(
            codename__in=["can_view_customer", "can_create_customer", "can_edit_customer", "can_delete_customer"]
        )
        self.user.user_permissions.add(*permissions)
        self.client.login(username="testuser", password="testpass123")

        self.product = Product.objects.create(name="Тестовая услуга", description="Описание", price=1000.00)
        self.lead = Lead.objects.create(
            first_name="Иван",
            last_name="Петров",
            phone="+7 999 123-45-67",
            email="ivan@example.com",
            is_converted=False,
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

    def test_customer_list_view(self):
        response = self.client.get(reverse("customers:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customers/customers-list.html")
        self.assertContains(response, "Петров Иван")

    def test_customer_detail_view(self):
        response = self.client.get(reverse("customers:detail", kwargs={"pk": self.customer.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "customers/customers-detail.html")

    def test_customer_create_view(self):
        # Создаем нового лида
        new_lead = Lead.objects.create(
            first_name="Петр",
            last_name="Сидоров",
            phone="+7 888 123-45-67",
            email="petr@example.com",
            is_converted=False,
        )
        new_contract = Contract.objects.create(
            name="Новый контракт",
            product=self.product,
            lead=new_lead,
            signing_date=date(2026, 2, 1),
            validity_period="24 месяца",
            amount=200000.00,
        )
        response = self.client.post(
            reverse("customers:create"), {"lead": new_lead.pk, "contract": new_contract.pk, "is_active": True}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Customer.objects.count(), 2)
        # Проверяем, что лид отмечен как переведённый
        new_lead.refresh_from_db()
        self.assertTrue(new_lead.is_converted)

    def test_customer_delete_view(self):
        response = self.client.post(reverse("customers:delete", kwargs={"pk": self.customer.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Customer.objects.count(), 0)
        # Проверяем, что лид вернулся в статус "потенциальный"
        self.lead.refresh_from_db()
        self.assertFalse(self.lead.is_converted)
