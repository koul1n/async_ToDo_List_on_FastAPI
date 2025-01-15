#!/bin/bash


alembic revision --autogenerate -m "Auto migration"

alembic upgrade head

uvicorn run:app --host 0.0.0.0 --port 8000
