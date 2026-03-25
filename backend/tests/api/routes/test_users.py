from unittest.mock import patch
import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.models import UserCreate
from app import crud
from tests.utils.utils import random_email, random_lower_string


def test_get_users_superuser_me(client: TestClient, superuser_token_headers: dict[str, str]) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me",
                   headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"] is True
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_get_users_normal_user_me(client: TestClient, normal_user_token_headers: dict[str, str]) -> None:
    r = client.get(f"{settings.API_V1_STR}/users/me",
                   headers=normal_user_token_headers)
    currect_user = r.json()
    assert currect_user
    assert currect_user["is_active"] is True
    assert currect_user["is_superuser"] is False
    assert currect_user["email"] == settings.EMAIL_TEST_USER


def test_create_user_new_email(session: Session, client: TestClient, superuser_token_headers: dict[str, str]):
    with (
            patch("app.utils.send_email", return_value=None),
            patch("app.core.config.settings.SMTP_HOST", "smtp.example.com"),
            patch("app.core.config.settings.SMTP_USER", "admin@example.com"),
    ):
        username = random_email()
        password = random_lower_string()
        data = {"email": username, "password": password}
        r = client.post(
            f"{settings.API_V1_STR}/users/",
            headers=superuser_token_headers,
            json=data
        )
        assert 200 <= r.status_code < 300
        created_user = r.json()
        user = crud.get_user_by_email(session=session, email=username)
        assert user
        assert user.email == created_user["email"]


def test_get_existing_user_as_superuser(session: Session, client: TestClient, superuser_token_headers: dict[str, str]):
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.create_user(session=session, user_create=user_in)
    user_id = user.id
    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=superuser_token_headers
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.get_user_by_email(session=session, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]


def test_get_non_existing_user_as_superuser(client: TestClient, superuser_token_headers: dict[str, str]):
    r = client.get(f"{settings.API_V1_STR}/users/{uuid.uuid4()}",
                   headers=superuser_token_headers)
    assert r.status_code == 404
    assert r.json() == {"detail": "User not found"}


def test_get_existing_user_current_user(session: Session, client: TestClient):
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.create_user(session=session, user_create=user_in)
    user_id = user.id
    login_data = {
        "username": username,
        "password": password
    }

    r = client.post(
        f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}

    r = client.get(
        f"{settings.API_V1_STR}/users/{user_id}",
        headers=headers
    )
    assert 200 <= r.status_code < 300
    api_user = r.json()
    existing_user = crud.get_user_by_email(session=session, email=username)
    assert existing_user
    assert existing_user.email == api_user["email"]
