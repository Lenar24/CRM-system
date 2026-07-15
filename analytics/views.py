from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count, Sum
from django.views.generic import ListView

from ads.models import AdCampaign
from contracts.models import Contract


class AdCampaignStatisticView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Статистика рекламных кампаний"""

    model = AdCampaign
    template_name = "ads/ads-statistic.html"
    context_object_name = "ads"
    permission_required = "ads.can_view_adcampaign"

    def get_queryset(self):
        campaigns = AdCampaign.objects.annotate(
            leads_count=Count("leads", distinct=True), customers_count=Count("leads__customer", distinct=True)
        ).all()
        return campaigns

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for campaign in context["ads"]:
            total_revenue = (
                Contract.objects.filter(lead__campaign=campaign).aggregate(total=Sum("amount"))["total"] or 0
            )

            total_spent = campaign.budget or 0

            if total_spent > 0 and total_revenue > 0:
                campaign.profit = round(total_revenue / total_spent, 2)
            else:
                campaign.profit = "-" if total_spent == 0 else 0

        return context
