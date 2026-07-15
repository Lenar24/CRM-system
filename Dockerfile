# Dockerfile

FROM python:3.13-slim

# Создаем пользователя с именем appuser
RUN adduser --uid 1000 --disabled-password --gecos '' appuser

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем инструменты для анализа кода (если их нет в requirements)
RUN pip install --no-cache-dir pylint black isort pylint_django

# Копируем файлы конфигурации ДО копирования всего проекта
# Это позволяет использовать кэш Docker, если конфиги не менялись
COPY pyproject.toml .pylintrc ./

# Копируем весь проект
COPY . .

USER appuser

# Опционально: запускаем проверку кода при сборке
# RUN pylint CRM_system/ --score=n || exit 0

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
