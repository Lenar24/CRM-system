from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import Lead


class LeadForm(forms.ModelForm):
    phone = PhoneNumberField(
        region="RU",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Введите номер телефона (например: 8 999 123-45-67)"}
        ),
    )

    class Meta:
        model = Lead
        fields = ["first_name", "last_name", "phone", "email", "campaign"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите имя"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите фамилию"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Введите email"}),
            "campaign": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "phone": "Телефон",
            "email": "Email",
            "campaign": "Рекламная кампания",
        }
