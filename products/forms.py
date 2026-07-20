from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите название услуги"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 4, "placeholder": "Введите описание услуги"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Введите стоимость", "step": "0.01"}
            ),
        }
        labels = {
            "name": "Название услуги",
            "description": "Описание",
            "price": "Стоимость (₽)",
        }
