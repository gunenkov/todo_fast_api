from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Базовая схема пользователя
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)


# Схема для создания пользователя
class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


# Схема для обновления пользователя
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=8)


# Схема для ответа API
class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Схема для информации о текущем пользователе
class UserInfo(UserBase):
    ...

    class Config:
        from_attributes = True
