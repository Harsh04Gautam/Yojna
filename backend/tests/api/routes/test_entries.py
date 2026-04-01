from fastapi.testclient import TestClient
from app.core.config import settings
from tests.utils.utils import random_lower_string


def test_create_entries(client: TestClient, normal_user_token_headers: dict[str, str]):
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
    r = client.post(f"{settings.API_V1_STR}/events",
                    headers=normal_user_token_headers, json=data)
    event_id = r.json()["id"]
    r = client.post(f"{settings.API_V1_STR}/entries/{event_id}",
                    headers=normal_user_token_headers)
    assert r.status_code == 200
