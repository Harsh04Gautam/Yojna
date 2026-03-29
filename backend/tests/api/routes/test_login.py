from unittest.mock import patch

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.models import UserCreate
from app.core.security import verify_password
from app.utils import generate_password_reset_token
from app import crud
from tests.utils.utils import random_email, random_lower_string
from tests.utils.user import user_authentication_headers


def test_get_acess_token(client: TestClient):
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD
    }
    r = client.post(
        f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_incorrect_password(client: TestClient):
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": "incorrect"
    }
    r = client.post(
        f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == 400


def test_use_access_token(client: TestClient, superuser_token_headers: dict[str, str]):
    r = client.post(f"{settings.API_V1_STR}/login/test-token",
                    headers=superuser_token_headers)
    result = r.json()
    assert r.status_code == 200
    assert "email" in result


def test_recovery_password(client: TestClient, normal_user_token_headers: dict[str, str]):
    with (
            patch("app.core.config.settings.SMTP_HOST", "smtp.example.com"),
            patch("app.core.config.settings.SMTP_USER", "admin@example.com")
    ):
        email = "test@example.com"
        r = client.post(
            f"{settings.API_V1_STR}/password-recovery/{email}",
            headers=normal_user_token_headers
        )
        assert r.status_code == 200
        assert r.json() == {
            "message": "If that email is registered, we sent a password recovery link"
        }


def test_recovery_password_user_not_exists(client: TestClient, normal_user_token_headers: dict[str, str]):
    email = random_email()
    r = client.post(f"{settings.API_V1_STR}/password-recovery/{email}",
                    headers=normal_user_token_headers)
    assert r.status_code == 200
    assert r.json() == {
        "message": "If that email is registered, we sent a password recovery link"
    }


def test_reset_password(session: Session, client: TestClient):
    username = random_email()
    password = random_lower_string()
    new_password = random_lower_string()

    user_in = UserCreate(email=username, password=password)
    user = crud.create_user(session=session, user_create=user_in)
    token = generate_password_reset_token(email=username)
    data = {"new_password": new_password, "token": token}

    r = client.post(f"{settings.API_V1_STR}/reset-password",
                    json=data)
    assert r.status_code == 200
    assert r.json() == {"message": "Password updated successfully"}

    session.refresh(user)
    verified, _ = verify_password(new_password, user.hashed_password)
    assert verified


def test_reset_password_invalid_token(client: TestClient):
    data = {"new_password": "changethis", "token": "invalid"}
    r = client.post(f"{settings.API_V1_STR}/reset-password",
                    json=data)
    response = r.json()
    assert "detail" in response
    assert r.status_code == 400
    assert response["detail"] == "Invalid token"
