FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir uv

RUN uv sync --no-dev

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .
COPY entrypoint.sh .

RUN chmod +x entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]