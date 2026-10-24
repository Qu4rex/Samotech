FROM ghcr.io/astral-sh/uv:latest AS builder
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./

# Устанавливаем зависимости без разработки и без самого проекта
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-install-project

COPY . /app

# Устанавливаем сам проект
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev


# --- Финальный легкий образ (Runtime) ---
FROM python:3.12-slim-bookworm

WORKDIR /app

# Копируем виртуальное окружение и код из builder-этапа
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app /app

# Активируем виртуальное окружение через PATH
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 80

# Запуск FastAPI приложения
CMD ["fastapi", "run", "app/main.py", "--host", "0.0.0.0", "--port", "80"]
