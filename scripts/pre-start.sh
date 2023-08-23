#!/bin/bash

python /opt/service/pre_start.py && alembic upgrade head
/opt/service/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --reload
