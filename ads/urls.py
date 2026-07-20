from django.urls import path

from . import views

app_name = "ads"

urlpatterns = [
    path("", views.AdCampaignListView.as_view(), name="list"),
    path("<int:pk>/", views.AdCampaignDetailView.as_view(), name="detail"),
    path("new/", views.AdCampaignCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", views.AdCampaignUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", views.AdCampaignDeleteView.as_view(), name="delete"),
    path("statistic/", views.AdCampaignStatisticView.as_view(), name="statistic"),
]
