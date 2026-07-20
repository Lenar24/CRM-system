from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import models
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from contracts.models import Contract

from .forms import AdCampaignForm
from .models import AdCampaign


class AdCampaignListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Список рекламных кампаний"""

    model = AdCampaign
    template_name = "ads/ads-list.html"
    context_object_name = "ads"
    permission_required = "ads.can_view_adcampaign"
    paginate_by = 20

    def get_queryset(self):
        queryset = AdCampaign.objects.select_related("product").prefetch_related("leads").all()

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset


class AdCampaignDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Детальная страница кампании"""

    model = AdCampaign
    template_name = "ads/ads-detail.html"
    context_object_name = "campaign"
    permission_required = "ads.can_view_adcampaign"

    def get_queryset(self):
        return AdCampaign.objects.select_related("product").prefetch_related("leads").all()


class AdCampaignCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание кампании"""

    model = AdCampaign
    form_class = AdCampaignForm
    template_name = "ads/ads-create.html"
    permission_required = "ads.can_create_adcampaign"
    success_url = reverse_lazy("ads:list")

    def form_valid(self, form):
        messages.success(self.request, f'Кампания "{form.instance.name}" успешно создана!')
        return super().form_valid(form)


class AdCampaignUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование кампании"""

    model = AdCampaign
    form_class = AdCampaignForm
    template_name = "ads/ads-edit.html"
    permission_required = "ads.can_edit_adcampaign"
    success_url = reverse_lazy("ads:list")

    def form_valid(self, form):
        messages.success(self.request, f'Кампания "{form.instance.name}" успешно обновлена!')
        return super().form_valid(form)


class AdCampaignDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление кампании"""

    model = AdCampaign
    template_name = "ads/ads-delete.html"
    permission_required = "ads.can_delete_adcampaign"
    success_url = reverse_lazy("ads:list")

    def delete(self, request, *args, **kwargs):
        campaign = self.get_object()
        campaign_name = campaign.name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Кампания "{campaign_name}" успешно удалена!')
        return response


class AdCampaignStatisticView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Статистика рекламных кампаний"""

    model = AdCampaign
    template_name = "ads/ads-statistic.html"
    context_object_name = "ads"
    permission_required = "ads.can_view_adcampaign"

    def get_queryset(self):
        return (
            AdCampaign.objects.annotate(
                leads_count=models.Count("leads", distinct=True),
                customers_count=models.Count("leads__customer", distinct=True),
            )
            .select_related("product")
            .all()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for campaign in context["ads"]:
            total_revenue = (
                Contract.objects.filter(lead__campaign=campaign).aggregate(total=models.Sum("amount"))["total"] or 0
            )
            total_spent = campaign.budget or 0
            campaign.profit = round(total_revenue / total_spent, 2) if total_spent > 0 else "-"

        return context
