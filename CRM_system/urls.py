"""
URL configuration for CRM_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("users.urls")),  # Главная страница (users/index.html)
    path("products/", include("products.urls")),  # Услуги
    path("ads/", include("ads.urls")),  # Рекламные кампании
    path("leads/", include("leads.urls")),  # Потенциальные клиенты
    path("contracts/", include("contracts.urls")),  # Контракты
    path("customers/", include("customers.urls")),  # Активные клиенты
    path("analytics/", include("analytics.urls")),  # Статистика
    path("accounts/", include("registration.urls")),  # Регистрация/авторизация
]

# Для разработки: раздаём статические и медиа-файлы
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
