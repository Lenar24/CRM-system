from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import render

from ads.models import AdCampaign
from customers.models import Customer
from leads.models import Lead
from products.models import Product


@login_required  # ← Это заставляет переходить на страницу входа
def index(request):
    """Главная страница с общей статистикой"""
    # Кешируем статистику на 5 минут
    cache_key = "main_statistics"
    context = cache.get(cache_key)

    if context is None:
        # Используем только count() для уменьшения нагрузки
        context = {
            "products_count": Product.objects.count(),
            "advertisements_count": AdCampaign.objects.count(),
            "leads_count": Lead.objects.count(),
            "customers_count": Customer.objects.count(),
        }
        cache.set(cache_key, context, 300)  # 5 минут

    return render(request, "users/index.html", context)
