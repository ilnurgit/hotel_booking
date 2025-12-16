"""
Корневой URL-конфиг проекта.

Назначение:
- /admin/ — административная панель Django
- /api/    — публичное REST API проекта (приложение hotels)

Все бизнес-эндпоинты проекта подключаются через hotels.urls,
чтобы корневой конфиг оставался максимально тонким.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Админка Django
    path("admin/", admin.site.urls),
    # REST API проекта
    path("api/", include("hotels.urls")),
]
