from django import forms

from leads.models import Lead

from .models import Customer


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["lead", "contract", "is_active"]
        widgets = {
            "lead": forms.Select(attrs={"class": "form-select"}),
            "contract": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "lead": "Потенциальный клиент",
            "contract": "Контракт",
            "is_active": "Активен",
        }
        help_texts = {
            "lead": "Выберите потенциального клиента (только не переведённые)",
            "contract": "Выберите контракт для клиента",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Показываем только лидов, которые ещё не переведены в активных
        self.fields["lead"].queryset = Lead.objects.filter(is_converted=False)
