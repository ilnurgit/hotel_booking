# Hotel Booking API (Django + DRF)

REST API для управления **категориями номеров**, **номерами** и **бронированиями**.

Проект демонстрирует:
- работу с Django REST Framework,
- PostgreSQL-ограничения (включая `ExclusionConstraint` против пересечений броней),
- конфигурацию через переменные окружения (`pydantic-settings`),
- запуск в Docker,
- качество кода через `ruff + mypy + pytest`,
- CI в GitHub Actions.

---

## Стек

- Python 3.12
- Django 6.0 + Django REST Framework
- PostgreSQL (обязателен, т.к. используется `ExclusionConstraint` и `btree_gist`)
- Docker / Docker Compose
- ruff, mypy, pytest, pre-commit
- pydantic-settings (загрузка конфигурации из `.env` / env)

---

## Логика бронирований

Используется логика интервала **`[start, end)`**:

- `date_start` **включительно**
- `date_end` **не включительно**

Пример:
- Бронь 20 → 25 и бронь 25 → 27 **не пересекаются** и разрешены.

Защита от пересечений реализована на уровне базы PostgreSQL через:
- `ExclusionConstraint` по `room` и `tstzrange(date_start, date_end, '[)')`
- расширение `btree_gist` (ставится миграцией автоматически)

---

## Запуск через Docker

### 1) Переменные окружения

Создай файл `.env` в корне проекта (рядом с `docker-compose.yml`):

```env
DJANGO_SECRET_KEY=super-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

POSTGRES_DB=hotel_booking
POSTGRES_USER=hotel_booking
POSTGRES_PASSWORD=hotel_booking
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### 2) Запуск контейнеров

```bash
docker compose up --build
```

API будет доступно на `http://127.0.0.1:8000/`

---

## API Endpoints

Базовый префикс: `/api/`

### Health-check
`GET /api/ping/`

```json
{"status": "ok"}
```

### Категории
- `GET /api/categories/`
- `POST /api/categories/`

### Номера
- `GET /api/rooms/`
- `POST /api/rooms/`
- `DELETE /api/rooms/<id>/`

### Бронирования
- `POST /api/bookings/`
- `DELETE /api/bookings/<id>/`
- `GET /api/rooms/<room_id>/bookings/`

---

## Тесты

```bash
poetry run pytest
```

---

## Качество кода

```bash
poetry run ruff check .
poetry run ruff format --check .
poetry run mypy .
```

---

## CI

В проекте настроен GitHub Actions CI:
- ruff
- mypy
- pytest
