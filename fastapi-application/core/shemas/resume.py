from datetime import datetime
from pydantic import BaseModel


class ResumeBase(BaseModel):
    title: str
    content: str


class ResumeCreate(ResumeBase):
    pass


class ResumeUpdate(BaseModel):
    title: str | None = None
    content: str | None = None


class ResumeRead(ResumeBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
