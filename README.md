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



# Мотивация участия в проекте, для которого выполенно это тестовое задание:

### 1. Почему тебе интересен этот проект? 

```
Мне интересен проект, потому что он решает не абстрактную задачу, а реальную боль сотрудников: ручная проверка документов отнимает много времени и несёт риски ошибок, а автоматизация через API и версионность делает процессы прозрачными и безопасными.

Особенно ценно, что бэкенд здесь — это не просто «прослойка», а ядро, которое обеспечивает целостность данных, аудит и интеграцию с AI‑модулем.

Отдельно привлекает техническая часть: FastAPI, PostgreSQL, SQLAlchemy, Alembic, Pydantic — это стек, с которым я хочу уверенно работать на практике.

Задачи вроде валидации по паттернам, управления версиями, корректной обработки ошибок и покрытия тестами (pytest) как раз позволяют прокачать навыки, которые важны и для коммерческой разработки, и для собственных проектов.

```

### 2. Как ты видишь свою роль в команде, которая создаёт продукт?

```

Я вижу себя как Backend‑разработчика, который отвечает за надёжность и предсказуемость API: чтобы каждый эндпоинт возвращал понятные статусы, данные сохранялись корректно, а логика валидации работала чётко и прозрачно.

Буду реализовывать ключевые сценарии: загрузку пакетов, определение типов документов по имени, проверку комплектности, формирование итогового статуса (approved/rejected/check_in_progress) и ведение истории изменений.

Также готов участвовать в проектировании схемы БД и миграций, писать тесты (в том числе для определения типа документа и расчёта статуса), поддерживать документацию (README, переменные окружения, архитектура) и помогать с контейнеризацией (Docker, docker-compose), чтобы проект можно было поднять одной командой.

```

### 3. Сколько времени в неделю ты готова уделять проекту и в течение какого периода?

```

Могу стабильно уделять 20-30 часов в неделю и выше, если появятся срочные задачи или нужно будет закрыть важный этап. Готова работать по проекту такой срок, который потребуется для решения поставленных задач, даже если это будет дольше, чем было изначально заявлено(1,5-2 месяца).

```
