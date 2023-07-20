FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11-2023-07-17

ENV PYTHONUNBUFFERED 1

COPY requirements /requirements
RUN pip install -r /requirements/requirements.txt

WORKDIR /app
COPY . .
