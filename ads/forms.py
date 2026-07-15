from django import forms

from .models import AdCampaign


class AdCampaignForm(forms.ModelForm):
    class Meta:
        model = AdCampaign
        fields = ["name", "product", "channel", "budget", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите название кампании"}),
            "product": forms.Select(attrs={"class": "form-select"}),
            "channel": forms.Select(attrs={"class": "form-select"}),
            "budget": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Введите бюджет", "step": "0.01"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name": "Название кампании",
            "product": "Рекламируемая услуга",
            "channel": "Канал продвижения",
            "budget": "Бюджет (₽)",
            "is_active": "Активна",
        }
        help_texts = {
            "name": "Уникальное название кампании",
            "budget": "Укажите бюджет в рублях",
        }
