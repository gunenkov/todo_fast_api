from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


# Базовая схема для заметки
class TodoBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    is_completed: bool = False


# Схема для создания заметки
class TodoCreate(TodoBase):
    pass


# Схема для обновления заметки
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    is_completed: Optional[bool] = None


# Схема для ответа API
class TodoResponse(TodoBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
