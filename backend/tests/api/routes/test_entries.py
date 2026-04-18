from datetime import datetime, timedelta
from dateutil.rrule import rrulestr
from fastapi.testclient import TestClient
from app.core.config import settings
from tests.utils.utils import random_lower_string


def test_create_entries(client: TestClient, normal_user_token_headers: dict[str, str], random_event):
    event, blocks = random_event()
    event_id = event.id

    rrule = rrulestr(event.rrule)
    occurrences = rrule.between(
        after=event.start_at - timedelta(days=5),
        before=event.start_at + timedelta(days=5),
        inc=True
    )

    data = {
        "data": {
            blocks[0]: random_lower_string(),
            blocks[1]: 20,
            blocks[2]: True,
        },
        "scheduled_at": str(occurrences[0])
    }

    r = client.post(f"{settings.API_V1_STR}/entries/{event_id}",
                    headers=normal_user_token_headers, json=data)
    assert r.status_code == 200


def test_create_entries_incorrect_time(client: TestClient, normal_user_token_headers: dict[str, str], random_event):
    event, blocks = random_event()
    event_id = event.id

    data = {
        "data": {
            blocks[0]: random_lower_string(),
            blocks[1]: 20,
            blocks[2]: True,
        },
        "scheduled_at": str(datetime.now())
    }

    r = client.post(f"{settings.API_V1_STR}/entries/{event_id}",
                    headers=normal_user_token_headers, json=data)
    assert r.status_code == 400
    assert r.json()[
        "detail"] == "Invalid scheduled_at: Does not match event recurrence schedule."


def test_create_entries_duplicate(client: TestClient, normal_user_token_headers: dict[str, str], random_event):
    event, blocks = random_event()
    event_id = event.id

    rrule = rrulestr(event.rrule)
    occurrences = rrule.between(
        after=event.start_at - timedelta(days=5),
        before=event.start_at + timedelta(days=5),
        inc=True
    )

    data = {
        "data": {
            blocks[0]: random_lower_string(),
            blocks[1]: 20,
            blocks[2]: True,
        },
        "scheduled_at": str(occurrences[0])
    }

    r = client.post(f"{settings.API_V1_STR}/entries/{event_id}",
                    headers=normal_user_token_headers, json=data)
    r = client.post(f"{settings.API_V1_STR}/entries/{event_id}",
                    headers=normal_user_token_headers, json=data)
    assert r.status_code == 409
    assert r.json()[
        "detail"] == "An entry for this scheduled slot already exists."


def test_get_entries_by_event(client: TestClient, normal_user_token_headers: dict[str, str], random_event):
    event, blocks = random_event()
    event_id = event.id

    data = {
        "data": {
            blocks[0]: random_lower_string(),
            blocks[1]: 20,
            blocks[2]: True,
        },
        "scheduled_at": str(datetime.now())
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
            "scheduled_at": str(datetime.now())
        }

        client.post(f"{settings.API_V1_STR}/entries/{event_id}",
                    headers=normal_user_token_headers, json=data)

    start_date = datetime.now() - timedelta(days=10)
    end_date = datetime.now() + timedelta(days=10)

    r = client.get(f"{settings.API_V1_STR}/entries/calendar", headers=normal_user_token_headers, params={
        "start_date": start_date,
        "end_date": end_date,
        "event_id": event_id
    })

    print(r.url)
    print(r.json())

    assert r.status_code == 200
