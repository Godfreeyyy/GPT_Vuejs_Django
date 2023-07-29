from pydantic import BaseModel, Field
from ..models import User
from typing import Optional


class UserRequest(BaseModel):
    userId: int
    message: str


class AIResponse(BaseModel):
    message: Optional[str]
    users: Optional[User]

