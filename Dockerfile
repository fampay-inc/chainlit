FROM python:3.12-slim

# Basic Project setup
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PROJECT_SRC=/code

# Install system dependencies
RUN apt-get update && apt-get install -qq -y gettext build-essential --no-install-recommends

# Set working directory
WORKDIR $PROJECT_SRC

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/fampay-inc/chainlit.git@main

# Copy the rest of the project files
COPY . .

# Set the PATH to use the virtual environment (if needed)
ENV PATH="$PROJECT_SRC/venv/bin:$PATH"

# Scripts and config
WORKDIR /

# Command to initialize project
WORKDIR $PROJECT_SRC

RUN chmod +x scripts/launch.sh
ENTRYPOINT [ "scripts/launch.sh" ]

# Expose the necessary port
EXPOSE 8000
