FROM python:3.12-slim

# Basic Project setup
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PROJECT_SRC=/code

RUN apt-get update && apt-get install -qq -y gettext build-essential --no-install-recommends

WORKDIR $PROJECT_SRC
COPY ./pyproject.toml ./poetry.lock ./
ENV PATH="$POETRY_HOME/bin:$PATH"

# Dependency installation
RUN pip install poetry==1.8.3
RUN poetry install

## Scripts and config
WORKDIR /

# Codebase clone
COPY . $PROJECT_SRC

## Command to initialize project
WORKDIR $PROJECT_SRC

RUN chmod +x scripts/launch.sh
ENTRYPOINT [ "scripts/launch.sh" ]

# Port
EXPOSE 8000
