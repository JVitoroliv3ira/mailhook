from __future__ import annotations

from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship


class Message(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    from_addr: Optional[str] = Field(default=None, index=True, max_length=320)
    subject: Optional[str] = Field(default=None, index=True, max_length=400)
    size_bytes: int = 0
    has_text: bool = False
    has_html: bool = False
    raw_path: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.now, index=True)
    
    recipients: List["Recipient"] = Relationship(back_populates="message")
    attachments: List["Attachment"] = Relationship(back_populates="message")

class Recipient:
    id: Optional[int] = Field(default=None, primary_key=True)
    message_id: UUID = Field(foreign_key="message.id", index=True)
    kind: str = Field(max_length=3, index=True)
    address: str = Field(index=True, max_length=320)

    message: Message = Relationship(back_populates="recipients")

class Attachment:
    id: Optional[int] = Field(default=None, primary_key=True)
    message_id: UUID = Field(foreign_key="message.id", index=True)
    filename: Optional[str] = None
    content_type: Optional[str] = Field(default=None, index=True)
    size_bytes: int = 0
    stored_path: str
    sha256: str = Field(index=True)

    message: Message = Relationship(back_populates="attachments")

