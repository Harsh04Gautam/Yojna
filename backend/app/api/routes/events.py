import uuid
from fastapi import APIRouter, HTTPException, status

from app.api.deps import SessionDep, CurrentUser
from app.models import EventCreate, EventPublic, EventsPublic
from app import crud

router = APIRouter(prefix="/events", tags=["events"])


@router.post("/", response_model=EventPublic)
def create_event(session: SessionDep, event_in: EventCreate, current_user: CurrentUser):
    event = crud.create_event(
        session=session, event_create=event_in, user_id=current_user.id)
    return event


@router.get("/", response_model=EventsPublic)
def get_events(session: SessionDep, current_user: CurrentUser):
    events = crud.get_events(session=session, user_id=current_user.id)
    return events


@router.get("/{event_id}", response_model=EventPublic)
def get_events(session: SessionDep, event_id: uuid.UUID,  current_user: CurrentUser):
    event = crud.get_event(session=session, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    if event.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Event not found")
    return event
