from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import models
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from leads.models import Lead

from .forms import CustomerForm
from .models import Customer


class CustomerListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Список активных клиентов"""

    model = Customer
    template_name = "customers/customers-list.html"
    context_object_name = "customers"
    permission_required = "customers.can_view_customer"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                models.Q(lead__first_name__icontains=search)
                | models.Q(lead__last_name__icontains=search)
                | models.Q(lead__phone__icontains=search)
                | models.Q(lead__email__icontains=search)
            )
        return queryset


class CustomerDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Детальная страница клиента"""

    model = Customer
    template_name = "customers/customers-detail.html"
    context_object_name = "customer"  # ← для шаблона
    permission_required = "customers.can_view_customer"


class CustomerCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание активного клиента"""

    model = Customer
    form_class = CustomerForm
    template_name = "customers/customers-create.html"
    permission_required = "customers.can_create_customer"
    success_url = reverse_lazy("customers:list")

    def get_initial(self):
        """Если передан lead_id, предзаполняем поле lead"""
        initial = super().get_initial()
        lead_id = self.request.GET.get("lead_id")
        if lead_id:
            try:
                lead = Lead.objects.get(pk=lead_id, is_converted=False)
                initial["lead"] = lead
            except Lead.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        """При создании отмечаем лида как переведённого"""
        response = super().form_valid(form)
        # Отмечаем лида как переведённого
        lead = form.instance.lead
        lead.is_converted = True
        lead.save()
        messages.success(self.request, f'Клиент "{lead.get_full_name()}" успешно переведён в активные!')
        return response


class CustomerUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование клиента"""

    model = Customer
    form_class = CustomerForm
    template_name = "customers/customers-edit.html"
    permission_required = "customers.can_edit_customer"
    success_url = reverse_lazy("customers:list")

    def form_valid(self, form):
        messages.success(self.request, f'Клиент "{form.instance.get_full_name()}" успешно обновлен!')
        return super().form_valid(form)


class CustomerDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление клиента"""

    model = Customer
    template_name = "customers/customers-delete.html"
    permission_required = "customers.can_delete_customer"
    success_url = reverse_lazy("customers:list")

    def delete(self, request, *args, **kwargs):
        customer = self.get_object()
        customer_name = customer.get_full_name()
        # При удалении возвращаем лида в статус "потенциальный"
        lead = customer.lead
        lead.is_converted = False
        lead.save()
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Клиент "{customer_name}" успешно удален!')
        return response
