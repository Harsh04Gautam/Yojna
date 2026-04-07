import uuid
from fastapi import APIRouter, HTTPException, status
from app.api.deps import SessionDep, CurrentUser
from app import crud
from app.models import EntryCreate, EntriesPublic, EntryPublic

router = APIRouter(prefix="/entries", tags=["entries"])


@router.post("/{event_id}", response_model=EntryPublic)
def create_entries(session: SessionDep, current_user: CurrentUser, entry_in: EntryCreate, event_id: uuid.UUID):
    event = crud.get_event(session=session, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    if event.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Event not found")

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
