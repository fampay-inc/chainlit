FROM python:3.12-slim

# Basic Project setup
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PROJECT_SRC=/code

RUN apt-get update && apt-get install -qq -y gettext build-essential --no-install-recommends

# Set working directory
WORKDIR $PROJECT_SRC

# Copy the existing virtual environment from local system
COPY venv ./venv

# Set the PATH to use the copied virtual environment
ENV PATH="$PROJECT_SRC/venv/bin:$PATH"

# Copy the rest of the project files
COPY . .

## Scripts and config
WORKDIR /

# Command to initialize project
WORKDIR $PROJECT_SRC

RUN chmod +x scripts/launch.sh
RUN source venv/bin/activate
RUN pip install -r requirements.txt
ENTRYPOINT [ "scripts/launch.sh" ]

# Port
EXPOSE 8000
