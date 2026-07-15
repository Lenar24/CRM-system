from django.contrib.auth.models import User
from django.test import TestCase


class RegistrationLoginTest(TestCase):
    """Тесты для страницы входа"""

    def setUp(self):
        """Создание тестового пользователя"""
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_login_page_status_code(self):
        """Проверка, что страница входа доступна"""
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)

    def test_login_page_uses_correct_template(self):
        """Проверка, что используется правильный шаблон"""
        response = self.client.get("/accounts/login/")
        self.assertTemplateUsed(response, "registration/login.html")

    def test_successful_login(self):
        """Проверка успешного входа"""
        response = self.client.post("/accounts/login/", {"username": "testuser", "password": "testpass123"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/")

    def test_successful_login_redirects_to_next(self):
        """Проверка редиректа на указанную страницу после входа"""
        response = self.client.post(
            "/accounts/login/?next=/products/", {"username": "testuser", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 302)
        # Проверяем, что редирект на /products/
        self.assertEqual(response.url, "/products/")

    def test_failed_login(self):
        """Проверка неудачного входа (неверный пароль)"""
        response = self.client.post("/accounts/login/", {"username": "testuser", "password": "wrongpassword"})
        self.assertEqual(response.status_code, 200)
        # Проверяем наличие ошибки на странице (Django использует русский текст)
        self.assertContains(response, "Пожалуйста, введите правильные имя пользователя и пароль")

    def test_failed_login_wrong_username(self):
        """Проверка неудачного входа (неверное имя пользователя)"""
        response = self.client.post("/accounts/login/", {"username": "wronguser", "password": "testpass123"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Пожалуйста, введите правильные имя пользователя и пароль")


class RegistrationLogoutTest(TestCase):
    """Тесты для выхода из системы"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_logout_redirect(self):
        """Проверка редиректа после выхода (POST)"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.post("/accounts/logout/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/")

    def test_logout_clears_session(self):
        """Проверка, что сессия очищается после выхода"""
        self.client.login(username="testuser", password="testpass123")

        # Проверяем, что пользователь авторизован
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        # Выходим (POST)
        self.client.post("/accounts/logout/")

        # Проверяем, что пользователь больше не авторизован
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)


class RegistrationProtectedPagesTest(TestCase):
    """Тесты для защищённых страниц"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_home_page_requires_login(self):
        """Проверка, что главная страница требует авторизации"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_products_page_requires_login(self):
        """Проверка, что страница услуг требует авторизации"""
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_ads_page_requires_login(self):
        """Проверка, что страница рекламных кампаний требует авторизации"""
        response = self.client.get("/ads/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_authenticated_user_can_access_home(self):
        """Проверка, что авторизованный пользователь может видеть главную страницу"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)


class RegistrationIntegrationTest(TestCase):
    """Интеграционные тесты для регистрации"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_full_login_logout_flow(self):
        """Полный цикл: вход → просмотр страницы → выход (POST)"""
        # Вход
        self.client.post("/accounts/login/", {"username": "testuser", "password": "testpass123"})

        # Проверяем, что пользователь авторизован
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

        # Выход (POST)
        response = self.client.post("/accounts/logout/")
        self.assertEqual(response.status_code, 302)

        # Проверяем, что доступ к защищённой странице закрыт
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_login_with_redirect_to_next(self):
        """Вход с редиректом на конкретную страницу"""
        response = self.client.post(
            "/accounts/login/?next=/products/", {"username": "testuser", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/products/")
