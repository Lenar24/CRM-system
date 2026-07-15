from django.urls import path

from . import views

app_name = "analytics"

urlpatterns = [
    path("", views.AdCampaignStatisticView.as_view(), name="statistic"),
]
