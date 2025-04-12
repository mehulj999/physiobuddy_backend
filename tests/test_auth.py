# tests/test_auth.py
import pytest
from httpx import AsyncClient
from app.main import app
from app.database import SessionLocal
from app.models import User
import uuid


# Clean up test users before and after tests
def cleanup_test_users():
    db = SessionLocal()
    db.query(User).filter(User.email.like("testuser_%")).delete()
    db.commit()
    db.close()


@pytest.mark.asyncio
async def test_user_registration():
    cleanup_test_users()

    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    user_data = {
        "email": unique_email,
        "password": "testpassword123",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/register", json=user_data)
    
    assert response.status_code in (200, 201)


@pytest.mark.asyncio
async def test_duplicate_user_registration():
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    user_data = {
        "email": unique_email,
        "password": "testpassword123",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/register", json=user_data)
        response = await ac.post("/auth/register", json=user_data)

    assert response.status_code == 400
    assert "already registered" in response.text


@pytest.mark.asyncio
async def test_login():
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    user_data = {
        "email": unique_email,
        "password": "testpassword123",
    }

    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post("/auth/register", json=user_data)
        login_data = {"email": unique_email, "password": "testpassword123"}
        response = await ac.post("/auth/login", json=login_data)
    print(response.status_code)
    print(response.text)

    assert response.status_code == 200
    assert "access_token" in response.json()


# Clean up after all tests
def teardown_module(module):
    cleanup_test_users()
