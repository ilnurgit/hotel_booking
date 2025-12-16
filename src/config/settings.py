"""
Настройки Django-проекта hotel_booking.

Здесь мы не хардкодим конфигурацию (секреты, доступы к БД и т.п.),
а читаем её из переменных окружения через pydantic_settings
(см. config/app_settings.py).

Важно:
- В продакшене DJANGO_SECRET_KEY должен быть задан явно (не dev-значение).
- DEBUG в продакшене должен быть выключен.
"""

from pathlib import Path

from config.app_settings import settings as app

# Базовая директория проекта (src/)
BASE_DIR = Path(__file__).resolve().parent.parent

# Защита от случайного запуска "боевой" конфигурации с дефолтным секретом.
# В dev-режиме допускаем dev-secret-key, в prod — запрещаем.
if not app.debug and app.secret_key == "dev-secret-key":
    raise RuntimeError("DJANGO_SECRET_KEY must be set in production")

# --- Безопасность / базовые настройки Django ---
SECRET_KEY = app.secret_key
DEBUG = app.debug
ALLOWED_HOSTS: list[str] = app.allowed_hosts_list


# --- Приложения ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",  # Для Postgres-специфичных возможностей
    "rest_framework",  # Django REST Framework
    "hotels",
]

# --- Middleware ---
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# --- База данных ---
# Значения приходят из .env / переменных окружения через AppSettings.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": app.db_name,
        "USER": app.db_user,
        "PASSWORD": app.db_password,
        "HOST": app.db_host,
        "PORT": app.db_port,
    }
}


# --- Валидация паролей (стандарт Django) ---
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# --- Локализация / время ---
LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Europe/Moscow"
USE_I18N = True
USE_TZ = True


# --- Статика ---
STATIC_URL = "static/"

# --- Стандартное поле первичного ключа ---
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
