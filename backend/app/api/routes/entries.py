import uuid
from datetime import datetime
from dateutil.rrule import rrulestr
from enum import Enum
from pydantic import BaseModel
from sqlmodel import select, and_
from fastapi import APIRouter, HTTPException, status
from app.api.deps import SessionDep, CurrentUser
from app import crud
from app.models import EntryCreate, EntriesPublic, Entry

router = APIRouter(prefix="/entries", tags=["entries"])


class Status(str, Enum):
    COMPLETED = "completed"
    PENDING = "pending"


class CalendarSlot(BaseModel):
    scheduled_at: datetime
    status: Status
    entry_id: int | None = None
    event_id: uuid.UUID
    is_virtual: bool


def get_calendar_expansion(*, session: SessionDep, user_id: uuid.UUID, event_id: uuid.UUID, start: datetime, end: datetime):
    event = crud.get_event(session=session, event_id=event_id)
    if not event:
        return []

    rule = rrulestr(event.rrule, dtstart=event.start_at)

    upper_bound = min(end, event.end_at) if event.end_at else end
    expected_dates = rule.between(start, upper_bound, inc=True)

    statement = select(Entry).where(and_(Entry.event_id == event_id,
                                         Entry.user_id == user_id, Entry.scheduled_at >= start, Entry.scheduled_at <= end))
    entries = session.exec(statement).all()

    entry_map = {e.scheduled_at: e.id for e in entries}

    calendar = []
    for dt in expected_dates:
        entry_id = entry_map.get(dt)
        calendar.append(
            CalendarSlot(
                scheduled_at=dt,
                status=Status.COMPLETED if entry_id else Status.PENDING,
                entry_id=entry_id,
                event_id=event_id,
                is_virtual=entry_id is None
            )
        )
    return calendar


@router.get("/calendar", response_model=list[CalendarSlot])
def get_entries(session: SessionDep, current_user: CurrentUser, event_id: uuid.UUID, start_date: datetime, end_date: datetime):
    return get_calendar_expansion(session=session, user_id=current_user.id, event_id=event_id, start=start_date, end=end_date)


@router.post("/{event_id}")
def create_entries(session: SessionDep, current_user: CurrentUser, event_id: uuid.UUID, entry_in: EntryCreate):
    event = crud.get_event(session=session, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    if event.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Event not found")

    rrule = rrulestr(event.rrule, dtstart=event.start_at)
    last_occurence = rrule.before(entry_in.scheduled_at, inc=True)

    if last_occurence != entry_in.scheduled_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid scheduled_at: Does not match event recurrence schedule.")

    entry = crud.create_entry(
        session=session, entry_create=entry_in, event=event, user_id=current_user.id)
    return entry


@router.get("/{event_id}", response_model=EntriesPublic)
def get_entries(session: SessionDep, current_user: CurrentUser, event_id: uuid.UUID):
    event = crud.get_event(session=session, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    if event.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Event not found")

    entries = crud.get_entries_by_event(session=session, event_id=event_id)
    return entries
