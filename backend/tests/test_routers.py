import pytest
from fastapi.testclient import TestClient
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists

from backend import models
from backend.database import Base
from backend.routers import get_db
from main import app

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/rentomatic_test"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    if not database_exists:
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)
    yield engine


@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()

    # begin a non-ORM transaction
    connection.begin()

    # bind an individual Session to the connection
    db = Session(bind=connection)
    # db = Session(db_engine)
    app.dependency_overrides[get_db] = lambda: db

    yield db

    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c


def test_healthcheck(client):
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register(client):
    response = client.post(
        "/register",
        json={
            "fullname": "Test User",
            "email": "testuser@gmail.com",
            "mobile": "+919876543210",
            "password": "testpassword",
            "confirm_password": "testpassword",
            "license_number": "KA01 2021",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "status": "success",
        "message": "User registered successfully",
    }


def test_login(client, db):
    user = models.User(
        id=1,
        fullname="Test User",
        email="testuser@gmail.com",  # use the same email when creating the user
        mobile="+919876543210",
        hashed_password=pwd_context.hash("testpassword"),
        license_number="KA01 2021",
    )
    db.add(user)
    db.commit()
    response = client.post(
        "/login",
        json={
            "email": "testuser@gmail.com",  # and when trying to log in
            "password": "testpassword",
        },
    )
    assert response.json() == {
        "status": "success",
        "message": "Logged in successfully",
        "data": {
            "email": "testuser@gmail.com",
            "fullname": "Test User",
            "mobile": "+919876543210",
            "license_number": "KA01 2021",
            "id": 1,
        },
    }
    assert response.status_code == 200


def test_get_users(client, db):
    user1 = models.User(
        id=1,
        fullname="Test User 1",
        email="testuser1@gmail.com",
        mobile="+919876543211",
        hashed_password=pwd_context.hash("testpassword"),
        license_number="KA01 2021",
    )
    db.add(user1)
    user2 = models.User(
        id=2,
        fullname="Test User 2",
        email="testuser2@gmail.com",
        mobile="+919876543212",
        hashed_password=pwd_context.hash("testpassword"),
        license_number="KA01 2022",
    )
    db.add(user2)
    user3 = models.User(
        id=3,
        fullname="Test User 3",
        email="testuser3@gmail.com",
        mobile="+919876543213",
        hashed_password=pwd_context.hash("testpassword"),
        license_number="KA01 2023",
    )
    db.add(user3)
    db.commit()
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == [
        {
            "email": "testuser1@gmail.com",
            "fullname": "Test User 1",
            "mobile": "+919876543211",
            "license_number": "KA01 2021",
            "id": 1,
        },
        {
            "email": "testuser2@gmail.com",
            "fullname": "Test User 2",
            "mobile": "+919876543212",
            "license_number": "KA01 2022",
            "id": 2,
        },
        {
            "email": "testuser3@gmail.com",
            "fullname": "Test User 3",
            "mobile": "+919876543213",
            "license_number": "KA01 2023",
            "id": 3,
        },
    ]
