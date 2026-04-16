from datetime import datetime
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

    r = client.get(f"{settings.API_V1_STR}/entries/{event_id}",
                   headers=normal_user_token_headers)

    assert r.status_code == 200
