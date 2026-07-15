from django import forms

from .models import Contract


class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ["name", "product", "lead", "document", "signing_date", "validity_period", "amount"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите название контракта"}),
            "product": forms.Select(attrs={"class": "form-select"}),
            "lead": forms.Select(attrs={"class": "form-select"}),
            "document": forms.FileInput(attrs={"class": "form-control"}),
            "signing_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "validity_period": forms.TextInput(attrs={"class": "form-control", "placeholder": "Например: 12 месяцев"}),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Введите сумму", "step": "0.01"}
            ),
        }
        labels = {
            "name": "Название контракта",
            "product": "Услуга",
            "lead": "Клиент",
            "document": "Файл с документом",
            "signing_date": "Дата заключения",
            "validity_period": "Период действия",
            "amount": "Сумма контракта (₽)",
        }
        help_texts = {
            "validity_period": "Укажите период действия контракта (например: 12 месяцев)",
            "amount": "Укажите сумму в рублях",
        }
