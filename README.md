# Todo List API

REST API, разработанное в рамках подготовки мастер-класса на буткемп для начинающих Backend-разработчиков от Студенческой ИТ-лаборатории

**Стек:**

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/) (для Windows — [Docker Desktop](https://www.docker.com/products/docker-desktop/))

## Запуск приложения

### Docker Compose

1. Клонируйте репозиторий
2. Создайте в директории с файлом `docker-compose.yaml` файл `.env`, скопируйте в него содержимое файла `.env.example`
3. Настройте значения переменных окружения в файле `.env`

4. Для сборки и запуска контейнеров выполните команду:
```bash
docker-compose up --build
```

### Внешний экземпляр PostgreSQL

1. Установите интерпретатор Python (>=3.12)
2. Установите `poetry` в глобальное окружение интерпретатора командой:
```bash
pip install poetry
```
3. Перейдите в директорию с файлом `pypoetry.toml` и выполните из нее следующую команду для создания виртуального окружения и установки зависимостей:
```bash
poetry install
```
4. Создайте в этой же директории файл `.env`, скопируйте в него содержимое файла `.env.example`
5. Настройте значения переменных окружения в файле `.env`

6. Запустите приложение командой:
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Разработка

### Статический анализ типов и проверка форматирования кода

```bash
poetry run mypy . --explicit-package-base
poetry run black .
poetry run isort .
```

### Непрерывная интеграция (CI)

Проект настроен на автоматическую проверку форматирования кода с помощью [GitHub Actions](https://docs.github.com/ru/actions). При каждом пуше и pull request в ветки main или master будет запускаться синтаксический анализ кода с использованием [mypy](https://github.com/python/mypy), а также проверка форматирования кода с помощью [black](https://github.com/psf/black) и [isort](https://pycqa.github.io/isort/).

### Интерактивная документация

После запуска приложения интерактивная документация будет доступна по адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc


