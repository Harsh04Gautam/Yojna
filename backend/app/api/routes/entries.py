import uuid
from fastapi import APIRouter, HTTPException, status
from app.api.deps import SessionDep, CurrentUser
from app import crud

router = APIRouter(prefix="/entries", tags=["entries"])


@router.post("/{event_id}")
def create_entries(session: SessionDep, current_user: CurrentUser, event_id: uuid.UUID):
    event = crud.get_event(session=session, event_id=event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    if event.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Event not found")

    entry = crud.create_entry(session=session)
