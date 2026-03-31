from fastapi import APIRouter

from app.api.deps import SessionDep, CurrentUser
from app.models import EventCreate, EventPublic
from app import crud

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventPublic)
def create_event(session: SessionDep, event_in: EventCreate, current_user: CurrentUser):
    event = crud.create_event(
        session=session, event_create=event_in, user_id=current_user.id)
    return event


@router.get("/", response_model=list[EventPublic])
def get_events(session: SessionDep, current_user: CurrentUser):
    events = crud.get_events(session=session, user_id=current_user.id)
    return events
