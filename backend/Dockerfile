FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN pip install --upgrade pip && pip install fastapi uvicorn sqlalchemy psycopg[binary] alembic pydantic

COPY . /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
