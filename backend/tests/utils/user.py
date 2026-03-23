from fastapi.testclient import TestClient
from sqlmodel import Session
from pydantic import EmailStr

from app import crud
from app.models import UserCreate, UserUpdate
from app.core.config import settings
from tests.utils.utils import random_lower_string


def user_authentication_headers(client: TestClient, email: EmailStr, password: str):
    data = {"username": email, "password": password}
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(session: Session, client: TestClient, email: EmailStr):
    password = random_lower_string()
    user = crud.get_user_by_email(session=session, email=email)
    if not user:
        user_create = UserCreate(email=email, password=password)
        user = crud.create_user(session=session, user_create=user_create)
    else:
        user_update = UserUpdate(password=password)
        if not user.id:
            raise Exception("User id not set")
        user = crud.update_user(
            session=session, db_user=user, user_in=user_update)

    return user_authentication_headers(client=client, email=email, password=password)
