from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ProductForm
from .models import Product


class ProductListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Product
    template_name = "products/products-list.html"
    context_object_name = "products"
    permission_required = "products.can_view_product"
    paginate_by = 20

    def get_queryset(self):
        queryset = Product.objects.only("id", "name", "price").all()

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    template_name = "products/products-detail.html"
    context_object_name = "product"
    permission_required = "products.can_view_product"


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/products-create.html"
    permission_required = "products.can_create_product"
    success_url = reverse_lazy("products:list")

    def form_valid(self, form):
        messages.success(self.request, f'Услуга "{form.instance.name}" успешно создана!')
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "products/products-edit.html"
    permission_required = "products.can_edit_product"
    success_url = reverse_lazy("products:list")

    def form_valid(self, form):
        messages.success(self.request, f'Услуга "{form.instance.name}" успешно обновлена!')
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    template_name = "products/products-delete.html"
    permission_required = "products.can_delete_product"
    success_url = reverse_lazy("products:list")

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product_name = product.name
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f'Услуга "{product_name}" успешно удалена!')
        return response
