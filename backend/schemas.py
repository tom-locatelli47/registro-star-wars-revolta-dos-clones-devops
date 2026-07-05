from uuid import UUID

from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    done: bool | None = None
    img_attachment_key: UUID | None = None


class TaskOut(BaseModel):
    id: int
    title: str
    done: bool
    img_url: str | None = None

    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str
