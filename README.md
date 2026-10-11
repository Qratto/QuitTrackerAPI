# Quit Tracker API

REST API для отслеживания отказа от вредных привычек. Пользователи создают привычки, которые хотят бросить, отмечают срывы и получают статистику: текущую серию без срывов, рекорд и количество срывов.

## Стек

- Python 3.13
- FastAPI
- SQLAlchemy 2.0 (async) + asyncpg
- PostgreSQL 16
- Pydantic v2
- JWT-авторизация (`python-jose` + `argon2`)
- Docker + Docker Compose

## Быстрый старт через Docker

Самый простой способ — запустить всё одной командой. Нужен только установленный Docker.

### 1. Клонировать репозиторий

```bash
git clone https://github.com/username/quit-tracker.git
cd quit-tracker
```

### 2. Создать `.env`

Скопируй `.env.example` в `.env` и заполни значения:

```bash
cp .env.example .env
```

Минимально нужно:

```
DATABASE_USER=quit
DATABASE_PASSWORD=quit
DATABASE_HOST=db
DATABASE_PORT=5432
DATABASE_NAME=quit_tracker
SECRET_KEY=replace-with-a-long-random-string
```

**Важно:** `DATABASE_HOST=db` — это имя сервиса Postgres внутри `docker-compose.yml`. Если запускаешь без Docker, поставь `localhost`.

### 3. Запустить

```bash
docker compose up --build

```

### 4. Открыть Swagger

- Swagger UI: http://localhost:8000/docs

### Остановка

```bash
docker compose down
```

Остановить и удалить данные Postgres:

```bash
docker compose down -v
```

## Запуск локально без Docker

### 1. Создать venv и установить зависимости

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Запустить Postgres

Если Docker установлен, одной командой:

```bash
docker run --name quit-postgres \
    -e POSTGRES_USER=quit \
    -e POSTGRES_PASSWORD=quit \
    -e POSTGRES_DB=quit_tracker \
    -p 5432:5432 \
    -d postgres:16-alpine
```

### 3. Настроить `.env`

```
DATABASE_USER=quit
DATABASE_PASSWORD=quit
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=quit_tracker
SECRET_KEY=replace-with-a-long-random-string
```

### 4. Запустить приложение

```bash
uvicorn main:app --reload
```

### 5. Открыть Swagger

http://localhost:8000/docs

## Переменные окружения

| Переменная | Обязательна | Описание | Пример |
|---|---|---|---|
| `DATABASE_USER` | да | Пользователь Postgres | `quit` |
| `DATABASE_PASSWORD` | да | Пароль | `quit` |
| `DATABASE_HOST` | да | Хост БД. `db` для Docker, `localhost` локально | `db` |
| `DATABASE_PORT` | нет | Порт (по умолчанию `5432`) | `5432` |
| `DATABASE_NAME` | да | Имя базы | `quit_tracker` |
| `SECRET_KEY` | да | Ключ для подписи JWT | `c2VjcmV0...` |

`SECRET_KEY` можно сгенерировать:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

## Возможности

- **Регистрация и логин** по username/password, JWT-авторизация
- **Создание привычек**, которые бросаешь
- **Отметка срывов** с датой и заметкой
- **Статистика**: текущая серия без срывов, рекорд, количество срывов
- **Владение данными**: каждый пользователь видит только свои привычки
- **Админ-режим**: админ видит и редактирует данные всех пользователей
- **Управление пользователями**: список и просмотр (только для админов)

## Аутентификация

API использует **JWT Bearer** токены. Схема работы:

1. **Регистрация** — `POST /auth/register` создаёт пользователя.
2. **Логин** — `POST /auth/login` принимает `username` и `password` (в формате form-urlencoded), возвращает `access_token`.
3. **Защищённые запросы** — клиент передаёт токен в заголовке `Authorization: Bearer <token>`.


## Эндпоинты

### Сводная таблица

| Метод | Путь | Описание | Доступ | Успех |
|---|---|---|---|---|
| `GET` | `/health` | Проверка живости сервиса | публично | 200 |
| `POST` | `/auth/register` | Регистрация | публично | 201 |
| `POST` | `/auth/login` | Логин, получение токена | публично | 200 |
| `GET` | `/habits` | Список привычек | авторизация | 200 |
| `GET` | `/habits/{habit_id}` | Одна привычка | авторизация | 200 |
| `POST` | `/habits` | Создать привычку | авторизация | 201 |
| `PATCH` | `/habits/{habit_id}` | Обновить привычку | авторизация | 200 |
| `DELETE` | `/habits/{habit_id}` | Удалить привычку со срывами | авторизация | 204 |
| `GET` | `/habits/{habit_id}/stats` | Статистика по привычке | авторизация | 200 |
| `POST` | `/habits/{habit_id}/relapses` | Отметить срыв | авторизация | 201 |
| `GET` | `/habits/{habit_id}/relapses` | История срывов | авторизация | 200 |
| `GET` | `/users` | Список пользователей | только админ | 200 |
| `GET` | `/users/{user_id}` | Один пользователь | только админ | 200 |

**Админ vs обычный пользователь:**

- Обычный пользователь видит и меняет **только свои** привычки и срывы.
- Админ видит и меняет **все** привычки и срывы всех пользователей.
- Только админ может получать список пользователей.

---

### GET /health

Проверка работоспособности сервиса.

**Пример ответа**

HTTP code 200

```json
{
  "status": "ok"
}
```

---

### POST /auth/register

Регистрация нового пользователя.

**Тело запроса**

| Поле | Тип | Обязательно | Описание |
|---|---|---|---|
| `username` | `string` | да | Имя пользователя, уникальное |
| `password` | `string` | да | Пароль |

**Пример запроса**

```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "ivan",
    "password": "secret123"
  }'
```

**Пример ответа**

HTTP code 201

```json
{
  "id": 1,
  "username": "ivan",
  "is_admin": false
}
```

**Возможные ошибки**

- `409 Conflict` — такое имя уже занято

```json
{
  "message": "Username ivan already exists."
}
```

- `422 Unprocessable Entity` — невалидное тело запроса

---

### POST /auth/login

Логин. Принимает данные в формате `application/x-www-form-urlencoded` (стандарт OAuth2).

**Тело запроса**

| Поле | Тип | Обязательно | Описание |
|---|---|---|---|
| `username` | `string` | да | Имя пользователя |
| `password` | `string` | да | Пароль |

**Пример запроса**

```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=ivan&password=secret123"
```

**Пример ответа**

HTTP code 200

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Возможные ошибки**

- `401 Unauthorized` — неверный username или пароль

```json
{
  "message": "Unauthorized"
}
```

---

### GET /habits

Список привычек. Обычный пользователь получает только свои, админ — все.

**Заголовки**

```
Authorization: Bearer <token>
```

**Пример запроса**

```bash
curl http://localhost:8000/habits \
  -H "Authorization: Bearer eyJhbGci..."
```

**Пример ответа**

HTTP code 200

```json
[
  {
    "id": 1,
    "name": "Курение",
    "description": "Бросить окончательно",
    "started_at": "2026-09-01T00:00:00Z",
    "created_at": "2026-09-01T00:00:00Z"
  }
]
```

**Возможные ошибки**

- `401 Unauthorized` — токена нет или он невалиден

---

### GET /habits/{habit_id}

Получить одну привычку по id.

**Параметры пути**

| Параметр | Тип | Описание |
|---|---|---|
| `habit_id` | `integer` | ID привычки |

**Заголовки**

```
Authorization: Bearer <token>
```

**Пример запроса**

```bash
curl http://localhost:8000/habits/1 \
  -H "Authorization: Bearer eyJhbGci..."
```

**Пример ответа**

HTTP code 200

```json
{
  "id": 1,
  "name": "Курение",
  "description": "Бросить окончательно",
  "started_at": "2026-09-01T00:00:00Z",
  "created_at": "2026-09-01T00:00:00Z"
}
```

**Возможные ошибки**

- `401 Unauthorized` — токена нет или он невалиден
- `404 Not Found` — привычки с таким id нет или она принадлежит другому пользователю

```json
{
  "message": "Habit with id 1 not found"
}
```

---

### POST /habits

Создать привычку, которую бросаешь. Привычка привязывается к текущему пользователю.

**Заголовки**

```
Authorization: Bearer <token>
```

**Тело запроса**

| Поле | Тип | Обязательно | Описание |
|---|---|---|---|
| `name` | `string` | да | Название привычки |
| `description` | `string` | нет | Описание |

**Пример запроса**

```bash
curl -X POST http://localhost:8000/habits \
  -H "Authorization: Bearer eyJhbGci..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Курение",
    "description": "Бросить окончательно"
  }'
```

**Пример ответа**

HTTP code 201

```json
{
  "id": 1,
  "name": "Курение",
  "description": "Бросить окончательно",
  "started_at": "2026-09-01T00:00:00Z",
  "created_at": "2026-09-01T00:00:00Z"
}
```

**Возможные ошибки**

- `401 Unauthorized` — токена нет или он невалиден
- `422 Unprocessable Entity` — невалидное тело запроса

---

### PATCH /habits/{habit_id}

Частично обновить привычку. Передавай только те поля, которые нужно изменить.

**Параметры пути**

| Параметр | Тип | Описание |
|---|---|---|
| `habit_id` | `integer` | ID привычки |

**Заголовки**

```
Authorization: Bearer <token>
```

**Тело запроса**

| Поле | Тип | Обязательно | Описание |
|---|---|---|---|
| `name` | `string` | нет | Новое название |
| `description` | `string` | нет | Новое описание |

**Пример запроса**

```bash
curl -X PATCH http://localhost:8000/habits/1 \
  -H "Authorization: Bearer eyJhbGci..." \
  -H "Content-Type: application/json" \
  -d '{"name": "Курение (брошено)"}'
```

**Пример ответа**

HTTP code 200

```json
{
  "id": 1,
  "name": "Курение (брошено)",
  "description": "Бросить окончательно",
  "started_at": "2026-09-01T00:00:00Z",
  "created_at": "2026-09-01T00:00:00Z"
}
```

**Возможные ошибки**

- `401 Unauthorized` — токена нет или он невалиден
- `404 Not Found` — привычки с таким id нет или она принадлежит другому
- `422 Unprocessable Entity` — невалидное тело запроса

---

### DELETE /habits/{habit_id}

Удалить привычку вместе со всеми её срывами.

**Параметры пути**

| Параметр | Тип | Описание |
|---|---|---|
| `habit_id` | `integer` | ID привычки |

**Заголовки**

```
Authorization: Bearer <token>
```

**Пример запроса**

```bash
curl -X DELETE http://localhost:8000/habits/1 \
  -H "Authorization: Bearer eyJhbGci..."
```

**Пример ответа**

HTTP code 204

Тело ответа отсутствует.

**Возможные ошибки**

- `401 Unauthorized` — токена нет или он невалиден
- `404 Not Found` — привычки с таким id нет или она принадлежит другому

---

### GET /habits/{habit_id}/stats

Статистика по привычке: текущая серия, рекорд, количество срывов.

**Параметры пути**

| Параметр | Тип | Описание |
|---|---|---|
| `habit_id` | `integer` | ID привычки |

**Заголовки**

```
Authorization: Bearer <token>
```

**Как считается**

Серия — это интервал между соседними событиями. Точки на шкале времени: `started_at`, каждый `occurred_at` срыва, текущее время. `current_streak_days` — последний интервал, `longest_streak_days` — максимум по всем интервалам.

**Пример запроса**

```bash
curl http://localhost:8000/habits/1/stats \
  -H "Authorization: Bearer eyJhbGci..."
```

**Пример ответа (срывов нет)**

HTTP code 200

```json
{
  "habit_id": 1,
  "name": "Курение",
  "started_at": "2026-09-01T00:00:00Z",
  "last_relapse_at": null,
  "current_streak_days": 33,
  "longest_streak_days": 33,
  "relapse_count": 0
}
```

**Пример ответа (был один срыв)**

HTTP code 200

```json
{
  "habit_id": 1,
  "name": "Курение",
  "started_at": "2026-09-01T00:00:00Z",
  "last_relapse_at": "2026-09-21T12:00:00Z",
  "current_streak_days": 13,
  "longest_streak_days": 20,
  "relapse_count": 1
}
```

**Возможные ошибки**

- `401 Unauthorized` — токена нет или он невалиден
- `404 Not Found` — привычки с таким id нет или она принадлежит другому

---

### POST /habits/{habit_id}/relapses

Отметить срыв — момент, когда не удержался. Запись сохраняется с текущим временем UTC, если `occurred_at` не передан.

**Параметры пути**

| Параметр | Тип | Описание |
|---|---|---|
| `habit_id` | `integer` | ID привычки |

**Заголовки**

```
Authorization: Bearer <token>
```

**Тело запроса**

| Поле | Тип | Обязательно | Описание |
|---|---|---|---|
| `occurred_at` | `datetime` (ISO 8601) | нет | Когда произошёл срыв. По умолчанию — текущее время UTC |
| `note` | `string` | нет | Свободная заметка |

**Пример запроса**

```bash
curl -X POST http://localhost:8000/habits/1/relapses \
  -H "Authorization: Bearer eyJhbGci..." \
  -H "Content-Type: application/json" \
  -d '{
    "occurred_at": "2026-09-21T12:00:00Z",
    "note": "Стресс на работе"
  }'
```

**Пример ответа**

HTTP code 201

```json
{
  "id": 5,
  "habit_id": 1,
  "occurred_at": "2026-09-21T12:00:00Z",
  "note": "Стресс на работе",
  "created_at": "2026-09-21T12:05:33.123456Z"
}
```

**Возможные ошибки**

- `401 Unauthorized` — токена нет или он невалиден
- `404 Not Found` — привычки с таким id нет или она принадлежит другому
- `422 Unprocessable Entity` — невалидный формат `occurred_at`

---

### GET /habits/{habit_id}/relapses

История срывов по привычке. Сортировка — по времени срыва, от старых к новым.

**Параметры пути**

| Параметр | Тип | Описание |
|---|---|---|
| `habit_id` | `integer` | ID привычки |

**Заголовки**

```
Authorization: Bearer <token>
```

**Пример запроса**

```bash
curl http://localhost:8000/habits/1/relapses \
  -H "Authorization: Bearer eyJhbGci..."
```

**Пример ответа**

HTTP code 200

```json
[
  {
    "id": 3,
    "habit_id": 1,
    "occurred_at": "2026-09-10T18:30:00Z",
    "note": "Стресс на работе",
    "created_at": "2026-09-10T18:35:00Z"
  },
  {
    "id": 5,
    "habit_id": 1,
    "occurred_at": "2026-09-21T12:00:00Z",
    "note": null,
    "created_at": "2026-09-21T12:05:33Z"
  }
]
```

Если срывов нет — вернётся пустой массив `[]`.

**Возможные ошибки**

- `401 Unauthorized` — токена нет или он невалиден
- `404 Not Found` — привычки с таким id нет или она принадлежит другому

---

### GET /users

Список всех пользователей. **Только для администраторов.**

**Заголовки**

```
Authorization: Bearer <token>
```

**Пример запроса**

```bash
curl http://localhost:8000/users \
  -H "Authorization: Bearer eyJhbGci..."
```

**Пример ответа**

HTTP code 200

```json
[
  {
    "id": 1,
    "username": "ivan",
    "is_admin": false
  },
  {
    "id": 2,
    "username": "admin",
    "is_admin": true
  }
]
```

**Возможные ошибки**

- `401 Unauthorized` — токена нет или он невалиден
- `403 Forbidden` — пользователь не админ

```json
{
  "message": "Forbidden"
}
```

---

### GET /users/{user_id}

Получить одного пользователя по id. **Только для администраторов.**

**Параметры пути**

| Параметр | Тип | Описание |
|---|---|---|
| `user_id` | `integer` | ID пользователя |

**Заголовки**

```
Authorization: Bearer <token>
```

**Пример запроса**

```bash
curl http://localhost:8000/users/1 \
  -H "Authorization: Bearer eyJhbGci..."
```

**Пример ответа**

HTTP code 200

```json
{
  "id": 1,
  "username": "ivan",
  "is_admin": false
}
```

**Возможные ошибки**

- `401 Unauthorized` — токена нет или он невалиден
- `403 Forbidden` — пользователь не админ

---

## Коды ошибок

Все ошибки возвращаются в едином формате:

```json
{
  "message": "Описание ошибки"
}
```

| Код | Когда возникает |
|---|---|
| `401 Unauthorized` | Токена нет, он истёк или невалиден |
| `403 Forbidden` | Действие доступно только админам |
| `404 Not Found` | Привычка с таким id не найдена |
| `409 Conflict` | Username уже занят при регистрации |
| `422 Unprocessable Entity` | Невалидное тело запроса или параметры |
| `500 Internal Server Error` | Непредвиденная ошибка на сервере |
