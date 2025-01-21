FROM python:3.11-slim

WORKDIR /app


COPY . .


RUN poetry install --no-root



EXPOSE 8000
