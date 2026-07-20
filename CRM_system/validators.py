import re

from django.core.exceptions import ValidationError


# Валидатор для ФИО (только буквы и пробелы)
def validate_full_name(value):
    """Проверка, что ФИО содержит только буквы и пробелы"""
    if not re.match(r"^[а-яА-Яa-zA-Z\s\-]+$", value):
        raise ValidationError("ФИО должно содержать только буквы и пробелы")
