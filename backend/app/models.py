from functools import cache
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Literal, Optional, List, Annotated, Union
from enum import Enum
from zoneinfo import available_timezones

from sqlmodel import SQLModel, Field, Relationship, Column
from pydantic import EmailStr, BaseModel, field_validator
from sqlalchemy.dialects.postgresql import JSONB


def get_datetime_utc() -> datetime:
    return datetime.now(timezone.utc)


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=get_datetime_utc)
    events: list["Event"] = Relationship(
        back_populates="user", cascade_delete=True)


class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: str | None = None


class Message(SQLModel):
    message: str


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class BlockType(str, Enum):
    TEXT = "text"
    INPUT = "input"
    CHECKBOX = "checkbox"
    CODE = "code"


class BaseBlock(BaseModel):
    block_type: BlockType
    key: str
    label: str
    description: Optional[str] = None


class TextBlock(BaseBlock):
    block_type: Literal[BlockType.TEXT] = BlockType.TEXT
    description: str


class InputBlock(BaseBlock):
    block_type: Literal[BlockType.INPUT] = BlockType.INPUT
    input_type: Literal["text", "number", "date"] = "number"
    placeholder: Optional[str] = None


class CheckBoxBlock(BaseBlock):
    block_type: Literal[BlockType.CHECKBOX] = BlockType.CHECKBOX


class CodeBlock(BaseBlock):
    block_type: Literal[BlockType.CODE] = BlockType.CODE
    inputs: Dict[str, Any]
    script: str
    output: Dict[str, Any]


Block = Annotated[
    Union[TextBlock, InputBlock, CheckBoxBlock, CodeBlock],
    Field(discriminator="block_type")
]


class Phase(BaseModel):
    slug: str
    name: str
    blocks: List[Block]


class Blueprint(BaseModel):
    name: str
    phases: List[Phase]


@cache
def get_timezone() -> set[str]:
    return available_timezones()


class EventBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)
    is_active: bool = True

    blueprint: Dict[str, Any] = Field(sa_column=Column(JSONB))

    is_recurring: bool = Field(default=False)
    rrule: Optional[str] = Field(default=None, max_length=255)

    start_at: datetime = Field(default_factory=get_datetime_utc)
    duration_minutes: int = Field(default=30)
    timezone: str = Field(default="UTC")


class EventCreate(EventBase):
    pass


class EventUpdate(EventBase):
    title: str | None = Field(min_length=1, max_length=255)


class Event(EventBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=get_datetime_utc)
    user_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE")
    user: User | None = Relationship(back_populates="events")
    entries: list["Entry"] = Relationship(
        back_populates="event", cascade_delete=True)

    @field_validator("timezone", mode="after")
    @classmethod
    def validate_timezone(cls, v: str):
        if v not in get_timezone():
            raise ValueError(f"{v} is not a valid timezone")
        return v

    @field_validator("blueprint", mode="before")
    @classmethod
    def validate_blueprint_schema(cls, v: Any) -> Dict[str, Any]:
        if isinstance(v, dict):
            return Blueprint.model_validate(v).model_dump()

        if isinstance(v, Blueprint):
            return v.model_dump()

        return v


class EventPublic(EventBase):
    id: uuid.UUID
    created_at: datetime
    user_id: uuid.UUID


class EventsPublic(SQLModel):
    data: list[EventPublic]
    count: int


class EntryBase(SQLModel):
    data: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB))


class EntryCreate(EntryBase):
    pass


class Entry(EntryBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=get_datetime_utc)
    event_id: uuid.UUID = Field(
        foreign_key="event.id", nullable=False, ondelete="CASCADE")
    event: Event | None = Relationship(back_populates="entries")
