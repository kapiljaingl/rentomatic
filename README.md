1. Prerequisites to create a ReactJS application and call a backend API

A way to handle CORS:

How to create a fastapi application with simple healthcheck api and what are the package need to install ?

# Python Setup
python3.12 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn sqlalchemy psycopg2 "pydantic[email]" passlib bcrypt python-multipart

# Formatting
pip install pre-commit
pre-commit install

# Unittest
pip install pytest httpx
pip install sqlalchemy-utils

python -m pytest ./backend/tests/

# App run
uvicorn main:app --reload

# Prompt how to create a postgresql container ?
docker pull postgres
docker run --name rentomatic-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres  -p 5432:5432 -d postgres
docker exec -it rentomatic-postgres bash
psql -U postgres
CREATE DATABASE rentomatic;
\c rentomatic;

## FrontEnd

npx create-react-app frontend
export NODE_OPTIONS=--openssl-legacy-provider

npm install @material-ui/core

