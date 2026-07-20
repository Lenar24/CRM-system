"""
Представления для главной страницы CRM-системы.
"""

from django.shortcuts import render


def index(request):
    """
    Главная страница с общей статистикой.
    Отображает количество услуг, рекламных кампаний, лидов и активных клиентов.
    """
    return render(request, "users/index.html")
