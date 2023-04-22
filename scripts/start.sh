#!/bin/bash
echo "Running aplication..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload