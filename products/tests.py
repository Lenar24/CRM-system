from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

from .models import Product


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Тестовая услуга", description="Описание", price=1000.00)

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Тестовая услуга")
        self.assertEqual(self.product.price, 1000.00)

    def test_product_str(self):
        self.assertEqual(str(self.product), "Тестовая услуга")


class ProductViewsTest(TestCase):
    def setUp(self):
        # Создаем пользователя
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        # Добавляем ВСЕ необходимые разрешения
        permissions = Permission.objects.filter(
            codename__in=["can_view_product", "can_create_product", "can_edit_product", "can_delete_product"]
        )
        self.user.user_permissions.add(*permissions)

        # Логиним пользователя
        self.client.login(username="testuser", password="testpass123")

        # Создаем тестовый продукт
        self.product = Product.objects.create(name="Тестовая услуга", description="Описание", price=1000.00)

    def test_product_list_view(self):
        response = self.client.get(reverse("products:list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products-list.html")
        self.assertContains(response, "Тестовая услуга")

    def test_product_detail_view(self):
        response = self.client.get(reverse("products:detail", kwargs={"pk": self.product.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products-detail.html")

    def test_product_create_view(self):
        response = self.client.post(
            reverse("products:create"), {"name": "Новая услуга", "description": "Новое описание", "price": 2000.00}
        )
        self.assertEqual(response.status_code, 302)  # Редирект после создания
        self.assertEqual(Product.objects.count(), 2)

    def test_product_update_view(self):
        response = self.client.post(
            reverse("products:edit", kwargs={"pk": self.product.pk}),
            {"name": "Обновленная услуга", "description": "Новое описание", "price": 1500.00},
        )
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Обновленная услуга")

    def test_product_delete_view(self):
        response = self.client.post(reverse("products:delete", kwargs={"pk": self.product.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.count(), 0)


class ProductPermissionsTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Тестовая услуга", description="Описание", price=1000.00)

    def test_user_without_permissions(self):
        User.objects.create_user(username="nopermission", password="testpass123")
        self.client.login(username="nopermission", password="testpass123")

        response = self.client.get(reverse("products:list"))
        self.assertEqual(response.status_code, 403)

    def test_user_with_permissions(self):
        user = User.objects.create_user(username="withpermission", password="testpass123")
        permission = Permission.objects.get(codename="can_view_product")
        user.user_permissions.add(permission)
        self.client.login(username="withpermission", password="testpass123")

        response = self.client.get(reverse("products:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестовая услуга")
