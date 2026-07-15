from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "registration"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html", redirect_authenticated_user=True),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),  # ← Кастомный выход
]
