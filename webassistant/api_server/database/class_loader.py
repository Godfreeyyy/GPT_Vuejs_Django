from pydantic import BaseModel, Field
from typing import Optional, List


class User(BaseModel):
    id: Optional[int]
    avatar: Optional[str]
    name: Optional[str]

    def getName(self):
        return self.Name

    def getAvatar(self):
        return self.Avatar

    def getID(self):
        return self.Id


class ClassLoader(BaseModel):
    user: List[User]
