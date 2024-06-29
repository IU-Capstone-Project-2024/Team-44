# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.7
FROM python:${PYTHON_VERSION}-slim as base



RUN apt-get update && \
    apt-get -y install build-essential && \
    apt-get -y install gcc-11 g++-11 mono-mcs && \
    rm -rf /var/lib/apt/lists/*

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /rag_backend

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=./rag_backend/requirements.txt,target=./rag_backend/requirements.txt \
    python -m pip install -r ./rag_backend/requirements.txt

COPY . .

EXPOSE 8000

RUN python "./rag_backend/manage.py" migrate
CMD python "./rag_backend/manage.py" runserver 0.0.0.0:8000