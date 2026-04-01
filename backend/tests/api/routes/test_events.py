import uuid
from fastapi.testclient import TestClient
from app.core.config import settings
from tests.utils.utils import random_lower_string


def test_create_event(client: TestClient, normal_user_token_headers: dict[str, str]):
    data = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "blueprint": {
            "name": "Software Bug Fix",
            "phases": [
                    {
                        "name": "Discovery",
                        "blocks": [
                            {"key": "desc", "type": "text_box",
                                "label": "What is broken?"},
                            {"key": "severity", "type": "value_box",
                                "label": "Severity (1-5)"}
                        ]
                    },
                {
                        "name": "Resolution",
                        "blocks": [
                            {"key": "fix_details", "type": "text_box",
                                "label": "How was it fixed?"},
                            {"key": "verified", "type": "checkbox",
                                "label": "Tested in Prod?"}
                        ]
                    }
            ],
            "formula": "(severity * verified) / 5"
        }
    }

    r = client.post(f"{settings.API_V1_STR}/events/",
                    headers=normal_user_token_headers, json=data)
    assert r.status_code == 200
    event = r.json()
    assert event
    assert event["blueprint"]["phases"][0]["name"] == "Discovery"


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
    assert event["data"]
    assert event["count"] > 0


def test_get_event_by_id(client: TestClient, normal_user_token_headers: dict[str, str]):
    data = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "blueprint": {
            "block": random_lower_string()
        }
    }

    r = client.post(f"{settings.API_V1_STR}/events/",
                    headers=normal_user_token_headers, json=data)

    event_id = r.json()["id"]
    r = client.get(
        f"{settings.API_V1_STR}/events/{event_id}", headers=normal_user_token_headers)
    assert r.status_code == 200
    assert r.json()["title"] == data["title"]


def test_get_event_that_dose_not_exist(client: TestClient, normal_user_token_headers: dict[str, str]):
    r = client.get(
        f"{settings.API_V1_STR}/events/{uuid.uuid4()}", headers=normal_user_token_headers)
    assert r.status_code == 404
    assert r.json()["detail"] == "Event not found"


def test_get_event_unauthorized(client: TestClient, normal_user_token_headers: dict[str, str], superuser_token_headers: dict[str, str]):
    data = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "blueprint": {
            "block": random_lower_string()
        }
    }

    r = client.post(f"{settings.API_V1_STR}/events/",
                    headers=normal_user_token_headers, json=data)

    event_id = r.json()["id"]
    r = client.get(
        f"{settings.API_V1_STR}/events/{event_id}", headers=superuser_token_headers)
    assert r.status_code == 403
    assert r.json()["detail"] == "Event not found"
