from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import models
from django.shortcuts import redirect
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import LeadForm
from .models import Lead


class LeadListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Lead
    template_name = "leads/leads-list.html"
    context_object_name = "leads"
    permission_required = "leads.can_view_lead"
    paginate_by = 20

    def get_queryset(self):
        # Используем кеш для списка лидов
        cache_key = 'leads_list'
        queryset = cache.get(cache_key)

        if queryset is None:
            queryset = Lead.objects.select_related('campaign').all()
            cache.set(cache_key, queryset, 300)  # 5 минут

        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search) |
                models.Q(phone__icontains=search) |
                models.Q(email__icontains=search)
            )
            cache.delete(cache_key)

        return queryset


class LeadDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Lead
    template_name = "leads/leads-detail.html"
    context_object_name = "lead"
    permission_required = "leads.can_view_lead"


class LeadCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Lead
    form_class = LeadForm
    template_name = "leads/leads-create.html"
    permission_required = "leads.can_create_lead"
    success_url = reverse_lazy("leads:list")

    def form_valid(self, form):
        messages.success(self.request, f'Клиент "{form.instance.get_full_name()}" успешно создан!')
        cache.delete('leads_list')
        cache.delete('main_statistics')
        return super().form_valid(form)


class LeadUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = "leads/leads-edit.html"
    permission_required = "leads.can_edit_lead"
    success_url = reverse_lazy("leads:list")

    def form_valid(self, form):
        messages.success(self.request, f'Клиент "{form.instance.get_full_name()}" успешно обновлен!')
        cache.delete('leads_list')
        return super().form_valid(form)


class LeadDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Lead
    template_name = "leads/leads-delete.html"
    permission_required = "leads.can_delete_lead"
    success_url = reverse_lazy("leads:list")

    def delete(self, request, *args, **kwargs):
        lead = self.get_object()
        lead_name = lead.get_full_name()
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Клиент "{lead_name}" успешно удален!')
        cache.delete('leads_list')
        cache.delete('main_statistics')
        cache.delete('campaign_statistics')
        return response


class LeadConvertView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Представление для перевода лида в активного клиента"""

    model = Lead
    template_name = "leads/leads-convert.html"
    context_object_name = "lead"
    permission_required = "leads.can_convert_lead"

    def post(self, request, *args, **kwargs):
        lead = self.get_object()
        # Отмечаем лида как переведённого
        lead.is_converted = True
        lead.save()
        cache.delete('leads_list')
        cache.delete('main_statistics')
        cache.delete('campaign_statistics')
        messages.success(request, f'Клиент "{lead.get_full_name()}" переведен в активные!')
        # Перенаправляем на страницу создания активного клиента с предзаполненным lead_id
        return redirect(f"customers:create?lead_id={lead.pk}")
