#!/usr/bin/env bash

python -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

python -m playwright install

uvicorn app.main:app --host 0.0.0.0 --port 8000