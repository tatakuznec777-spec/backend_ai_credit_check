# Document Checker API

REST API сервис для проверки пакетов документов с сохранением истории в PostgreSQL.

# Быстрый старт

## Запуск через Docker

### Клонировать репозиторий
`git clone <repository-url>`

`cd backend_ai_credit_check`

### Скопировать переменные окружения
`cp .env.example .env`

### Запустить всё одной командой
`docker compose up --build`

### Или в фоне
`docker compose up --build -d`

## API будет доступен на http://localhost:8000

## Локальный запуск (для разработки):

### Установить зависимости
`uv sync`

### Запустить PostgreSQL
`docker run --name pg-local \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=doc_checker \
  -p 5432:5432 \
  -d postgres:16-alpine`

### Применить миграции
`uv run alembic upgrade head`

### Запустить сервер
`uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`



## Запуск тестов:

### Все тесты
`uv run pytest`

### С покрытием
`uv run pytest --cov=app`

### Только unit-тесты
`uv run pytest tests/unit/`

### Конкретный файл
`uv run pytest tests/unit/test_document_detector.py -v`



## API Endpoints

### Health Check

`curl http://localhost:8000/api/health`

### Список всех проверок

`curl http://localhost:8000/api/checks`

### Детали конкретной проверки

`curl http://localhost:8000/api/checks/{check_id}`

### Создать новую проверку

`curl -X POST http://localhost:8000/api/checks \
  -F "program=federal" \
  -F "files=@договор.pdf" \
  -F "files=@счёт.pdf" \
  -F "files=@акт.pdf" \
  -F "files=@спецификация.pdf"`

### Параметры:

program: federal или regional
files: файлы документов (PDF, DOCX, JPG, PNG, макс. 20 МБ каждый)

### Обязательные документы:

federal: договор, спецификация, счёт, акт
regional: договор, счёт, акт


## Формат ответа:

```{

  "check_id": "abc123e4-5678-90ab-cdef-ghijklmnopqr",

  "status": "rejected",

  "status_label": "Нельзя заявлять в банк",

  "reason": "Отсутствует спецификация к договору.",

  "issues": [

    {

      "level": "error",

      "message": "Отсутствует обязательный документ: спецификация"

    },

    {

      "level": "warning",

      "message": "Не удалось определить тип документа: «scan_0041.jpg»"

    }

  ],

  "documents": [

    {

      "name": "договор_47.pdf",

      "detected_type": "contract",

      "size_kb": 142

    }

  ],

  "extracted": {

    "contractor": "ООО «ТехАгро»",

    "amount": "1 250 000 ₽",

    "date": "01.03.2025",

    "subject": "Поставка минеральных удобрений"

  },

  "checked_at": "2025-03-15T14:32:00Z"

}

```


## Технологии:

```

Технология                                    Версия                              Зачем

Python                                        3.11                                Язык программирования

FastAPI                                       0.139                               Async веб-фреймворк

SQLAlchemy                                    2.0                                 ORM для работы с БД

PostgreSQL                                    16                                  Реляционная база данных

Alembic                                       1.18                                Миграции БД

Pydantic                                      2.13                                Валидация данных

Docker                                        29.x                                Контейнеризация

uv                                            0.11                                Быстрый менеджер пакетов

```


## Архитектура:

```

src/app/
├── api/v1/              # HTTP endpoints
│   └── endpoints/
│       ├── checks.py    # POST/GET /api/checks
│       └── health.py    # GET /api/health
├── core/                # Глобальные настройки
│   ├── config.py        # Pydantic settings
│   └── dependencies.py  # FastAPI dependencies
├── domain/              # Бизнес-логика
│   ├── checks/
│   │   ├── models.py    # SQLAlchemy модели
│   │   ├── schemas.py   # Pydantic схемы
│   │   ├── service.py   # Логика проверки
│   │   └── repository.py # CRUD операции
│   └── documents/
│       ├── detector.py  # Определение типа документа
│       ├── patterns.py  # Regex-паттерны
│       └── parser.py    # Извлечение данных
└── infrastructure/      # Внешние зависимости
    ├── database.py      # Подключение к БД
    └── security/        # Валидация файлов


```

## Безопасность

- Валидация расширений файлов

- Проверка размера файлов (макс. 20 МБ)

- Проверка magic bytes (python-magic)

- Непривилегированный пользователь в Docker

- Секреты только через .env

- Pydantic валидация входных данных


## Переменные окружения

_Скопируйте .env.example в .env и настройте:_

### Application
`DEBUG=true
API_V1_PREFIX=/api`

### Database
`POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=doc_checker`

### Upload limits
`MAX_FILE_SIZE_MB=20
MAX_FILES_PER_REQUEST=50`
