# syntax=docker/dockerfile:1.7

ARG PYTHON_VERSION=3.12
ARG UV_VERSION=0.8.22

# ---------------------------------------------------------
# uv binary
# ---------------------------------------------------------
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

# ---------------------------------------------------------
# Base image
# ---------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=uv /uv /uvx /bin/

# ---------------------------------------------------------
# Production dependencies
# ---------------------------------------------------------
FROM base AS prod-deps

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
        --locked \
        --no-dev \
        --no-install-project

# ---------------------------------------------------------
# Production build
# ---------------------------------------------------------
FROM prod-deps AS prod-build

COPY . .

# ---------------------------------------------------------
# Production runtime
# ---------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim-bookworm AS production

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    DJANGO_SETTINGS_MODULE=config.settings.production \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

RUN groupadd --system django \
    && useradd \
        --system \
        --gid django \
        --home-dir /app \
        --create-home \
        django

COPY --from=prod-build --chown=django:django /app /app

USER django

EXPOSE 8000

CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]

# ---------------------------------------------------------
# Development image
# ---------------------------------------------------------
FROM base AS development

ENV DJANGO_SETTINGS_MODULE=config.settings.development

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync \
        --locked \
        --dev \
        --no-install-project

COPY . .

EXPOSE 8000

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
