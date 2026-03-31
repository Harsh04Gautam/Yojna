from fastapi.testclient import TestClient
from app.core.config import settings
from tests.utils.utils import random_lower_string


def test_create_event(client: TestClient, normal_user_token_headers: dict[str, str]):
    data = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "blueprint": {
            "block": random_lower_string()
        }
    }

    r = client.post(f"{settings.API_V1_STR}/events/",
                    headers=normal_user_token_headers, json=data)
    assert r.status_code == 200
    event = r.json()
    assert event


def test_get_events(client: TestClient, normal_user_token_headers: dict[str, str]):
    data1 = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "blueprint": {
            "block": random_lower_string()
        }
    }

    data2 = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "blueprint": {
            "block": random_lower_string()
        }
    }

    client.post(f"{settings.API_V1_STR}/events/",
                headers=normal_user_token_headers, json=data1)
    client.post(f"{settings.API_V1_STR}/events/",
                headers=normal_user_token_headers, json=data2)

    r = client.get(f"{settings.API_V1_STR}/events/",
                   headers=normal_user_token_headers)
    assert r.status_code == 200
    event = r.json()
    assert event
    assert len(event) > 0
