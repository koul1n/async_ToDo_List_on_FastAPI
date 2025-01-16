#!/bin/bash


alembic revision --autogenerate -m "Auto migration"

alembic upgrade head

uvicorn run:app --host ${SERVER_HOST} --port ${SERVER_PORT}

