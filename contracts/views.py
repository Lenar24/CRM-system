from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ContractForm
from .models import Contract


class ContractListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """Список контрактов"""

    model = Contract
    template_name = "contracts/contracts-list.html"
    context_object_name = "contracts"  # ← для шаблона
    permission_required = "contracts.can_view_contract"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class ContractDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    """Детальная страница контракта"""

    model = Contract
    template_name = "contracts/contracts-detail.html"
    context_object_name = "contract"  # ← для шаблона
    permission_required = "contracts.can_view_contract"


class ContractCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание контракта"""

    model = Contract
    form_class = ContractForm
    template_name = "contracts/contracts-create.html"
    permission_required = "contracts.can_create_contract"
    success_url = reverse_lazy("contracts:list")

    def form_valid(self, form):
        messages.success(self.request, f'Контракт "{form.instance.name}" успешно создан!')
        return super().form_valid(form)


class ContractUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование контракта"""

    model = Contract
    form_class = ContractForm
    template_name = "contracts/contracts-edit.html"
    permission_required = "contracts.can_edit_contract"
    success_url = reverse_lazy("contracts:list")

    def form_valid(self, form):
        messages.success(self.request, f'Контракт "{form.instance.name}" успешно обновлен!')
        return super().form_valid(form)


class ContractDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление контракта"""

    model = Contract
    template_name = "contracts/contracts-delete.html"
    permission_required = "contracts.can_delete_contract"
    success_url = reverse_lazy("contracts:list")

    def delete(self, request, *args, **kwargs):
        contract = self.get_object()
        contract_name = contract.name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Контракт "{contract_name}" успешно удален!')
        return response
