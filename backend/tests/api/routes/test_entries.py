from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from app.core.config import settings
from tests.utils.utils import random_lower_string


def test_create_entries(client: TestClient, normal_user_token_headers: dict[str, str], random_event):
    event, blocks = random_event()
    event_id = event.id

    data = {
        "data": {
            blocks[0]: random_lower_string(),
            blocks[1]: 20,
            blocks[2]: True,
        },
        "due_date": str(datetime.now())
    }

    r = client.post(f"{settings.API_V1_STR}/entries/{event_id}",
                    headers=normal_user_token_headers, json=data)
    assert r.status_code == 200


def test_get_entries_by_event(client: TestClient, normal_user_token_headers: dict[str, str], random_event):
    event, blocks = random_event()
    event_id = event.id

    data = {
        "data": {
            blocks[0]: random_lower_string(),
            blocks[1]: 20,
            blocks[2]: True,
        },
        "due_date": str(datetime.now())
    }

    client.post(f"{settings.API_V1_STR}/entries/{event_id}",
                headers=normal_user_token_headers, json=data)

    r = client.get(f"{settings.API_V1_STR}/entries/{event_id}",
                   headers=normal_user_token_headers)

    assert r.status_code == 200
    assert r.json()["data"]
    assert r.json()["count"] > 0


def test_get_calendar(client: TestClient, normal_user_token_headers: dict[str, str], random_event):
    event, blocks = random_event()
    event_id = event.id

    for _ in range(5):
        data = {
            "data": {
                blocks[0]: random_lower_string(),
                blocks[1]: 20,
                blocks[2]: True,
            },
            "due_date": str(datetime.now())
        }

        client.post(f"{settings.API_V1_STR}/entries/{event_id}",
                    headers=normal_user_token_headers, json=data)

    start_date = (datetime.now() - timedelta(days=1)).isoformat()
    end_date = (datetime.now() + timedelta(days=10)).isoformat()

    r = client.get(f"{settings.API_V1_STR}/entries/calendar", headers=normal_user_token_headers, params={
        "start_date": start_date,
        "end_date": end_date,
        "event_id": event_id
    })

    print(r.url)
    print(r.json())

    assert r.status_code == 200
