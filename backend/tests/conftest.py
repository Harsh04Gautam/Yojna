import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.db import engine, init_db
from app.core.config import settings
from app.models import User, Event
from app.main import app
from tests.utils.user import authentication_token_from_email
from utils.utils import get_superuser_token_headers
from tests.utils.events import create_random_event


@pytest.fixture(scope="session", autouse=True)
def session():
    with Session(engine) as session:
        init_db(session)
        yield session
        session.exec(delete(User))
        session.commit()


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def superuser_token_headers(client: TestClient):
    return get_superuser_token_headers(client)


@pytest.fixture
def normal_user_token_headers(session: Session, client: TestClient):
    return authentication_token_from_email(session=session, client=client, email=settings.EMAIL_TEST_USER)


@pytest.fixture
def random_event(session: Session):
    def _create() -> (Event, list[str]):
        return create_random_event(session=session)
    return _create
