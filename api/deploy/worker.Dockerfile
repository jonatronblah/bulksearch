FROM python:3.11.5-slim-bullseye as prod
RUN apt-get update && apt-get install -y --no-install-recommends \
  gcc \
  unixodbc-dev \
  unixodbc \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*


RUN pip install poetry==1.6.1

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install --only main
# Removing gcc
RUN apt-get purge -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Copying actuall application
COPY . /app/src/
RUN poetry install --only main

CMD ["/usr/local/bin/python", "-m", "client_bulksearch"]

FROM prod as dev

# COPY clients.csv /dev/clients.csv

RUN poetry install
