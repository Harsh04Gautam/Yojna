from datetime import datetime
from fastapi.testclient import TestClient
from app.core.config import settings
from tests.utils.utils import random_lower_string


def test_create_entries(client: TestClient, normal_user_token_headers: dict[str, str]):
    phase_key = [random_lower_string(), random_lower_string(),
                 random_lower_string()]
    data = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "is_active": True,
        "phases": [
            {
                "slug": random_lower_string(),
                "name": random_lower_string(),
                "blocks": [
                    {
                        "block_type": "text",
                        "key": phase_key[0],
                        "label": random_lower_string(),
                        "description": random_lower_string()
                    },
                    {
                        "block_type": "input",
                        "key": phase_key[1],
                        "label": random_lower_string(),
                        "description": random_lower_string(),
                        "input_type": "number",
                        "placeholder": random_lower_string()
                    },
                    {
                        "block_type": "checkbox",
                        "key": phase_key[2],
                        "label": random_lower_string(),
                        "description": random_lower_string(),
                    },
                ]
            }
        ],
    }

    r = client.post(f"{settings.API_V1_STR}/events",
                    headers=normal_user_token_headers, json=data)
    event_id = r.json()["id"]

    data = {
        "data": {
            phase_key[0]: random_lower_string(),
            phase_key[1]: 20,
            phase_key[2]: True,
        },
        "due_date": str(datetime.now())
    }

    r = client.post(f"{settings.API_V1_STR}/entries/{event_id}",
                    headers=normal_user_token_headers, json=data)
    assert r.status_code == 200
