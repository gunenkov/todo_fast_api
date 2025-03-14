FROM python:3.12-slim as builder

WORKDIR /todo_api

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry && poetry config virtualenvs.in-project true && poetry install --no-cache --only main

FROM python:3.12-slim

COPY --from=builder /todo_api /todo_api

COPY . .

CMD ["/todo_api/.venv/bin/python", "/todo_api/.venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
