from sqlmodel import Session

from app import crud
from app.models import EventCreate, Event
from app.core.config import settings
from tests.utils.utils import random_lower_string


def create_random_event(session: Session) -> (Event, list[str]):
    blocks = [random_lower_string() for _ in range(3)]
    user = crud.get_user_by_email(
        session=session, email=settings.EMAIL_TEST_USER)
    data = {
        "title": random_lower_string(),
        "description": random_lower_string(),
        "is_active": True,
        "is_recurring": True,
        "rrule": "FREQ=DAILY;INTERVAL=10;COUNT=5",
        "phases": [
            {
                "slug": random_lower_string(),
                "name": random_lower_string(),
                "blocks": [
                    {
                        "block_type": "text",
                        "key": blocks[0],
                        "label": random_lower_string(),
                        "description": random_lower_string()
                    },
                    {
                        "block_type": "input",
                        "key": blocks[1],
                        "label": random_lower_string(),
                        "description": random_lower_string(),
                        "input_type": "number",
                        "placeholder": random_lower_string()
                    },
                    {
                        "block_type": "checkbox",
                        "key": blocks[2],
                        "label": random_lower_string(),
                        "description": random_lower_string(),
                    },
                ]
            }
        ],
    }

    event_create = EventCreate(**data)
    event = crud.create_event(
        session=session, event_create=event_create, user_id=user.id)
    return event, blocks
