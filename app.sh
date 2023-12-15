#!/bin/bash

echo "STARTING SERVER"
pip install uvicorn[standard]
uvicorn instagram.asgi:application --host 0.0.0.0 --port 8000 --workers 4


