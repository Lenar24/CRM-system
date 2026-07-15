from django.contrib.auth.models import User
from django.test import TestCase

from ads.models import AdCampaign
from products.models import Product


class UsersViewsTest(TestCase):
    """Тесты для представлений users"""

    def setUp(self):
        """Создание тестового пользователя"""
        self.user = User.objects.create_user(username="testuser", password="testpass123")

        # Создаем тестовые данные для статистики
        self.product = Product.objects.create(name="Тестовая услуга", description="Описание", price=1000.00)
        self.campaign = AdCampaign.objects.create(
            name="Тестовая кампания", product=self.product, channel="social", budget=5000.00
        )

    def test_home_page_status_code(self):
        """Проверка, что главная страница доступна"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        """Проверка, что используется правильный шаблон"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/")
        self.assertTemplateUsed(response, "users/index.html")

    def test_home_page_without_login(self):
        """Неавторизованный пользователь должен быть перенаправлен"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_home_page_contains_statistics(self):
        """Проверка, что на главной странице есть статистика"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/")
        self.assertContains(response, "1")  # Количество продуктов = 1

    def test_home_page_context(self):
        """Проверка контекста главной страницы"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/")
        self.assertEqual(response.context["products_count"], 1)
        self.assertEqual(response.context["advertisements_count"], 1)

    def test_login_page(self):
        """Проверка страницы входа"""
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)

    def test_successful_login(self):
        """Проверка успешного входа"""
        response = self.client.post("/accounts/login/", {"username": "testuser", "password": "testpass123"})
        self.assertEqual(response.status_code, 302)  # Редирект после входа

    def test_failed_login(self):
        """Проверка неудачного входа"""
        response = self.client.post("/accounts/login/", {"username": "testuser", "password": "wrongpassword"})
        self.assertEqual(response.status_code, 200)  # Страница входа с ошибкой


class UsersUrlsTest(TestCase):
    """Тесты для URL-адресов users"""

    def test_urls_resolve(self):
        """Проверка, что URL-адреса разрешаются правильно"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)  # Требует авторизации
