#!/bin/sh

#echo "Running pytests..."
#pytest tests/test_routes_simple.py || exit 1


#echo "Running unittests..."
#python -m unittest tests/test_routes.py || exit 1

echo "Starting app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
