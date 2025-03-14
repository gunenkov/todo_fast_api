from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate


class TodoService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_by_id(self, todo_id: int) -> Optional[Todo]:
        """Получает заметку по ID."""
        result = await self.db.execute(select(Todo).filter(Todo.id == todo_id))
        return result.scalars().first()

    async def get_by_user_id(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Todo]:
        """Получает все заметки пользователя с пагинацией."""
        result = await self.db.execute(
            select(Todo).filter(Todo.user_id == user_id).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, todo_in: TodoCreate, user_id: int) -> Todo:
        """Создает новую заметку."""
        # Создаем объект заметки
        todo = Todo(**todo_in.model_dump(), user_id=user_id)

        # Добавляем заметку в БД
        self.db.add(todo)
        await self.db.commit()
        await self.db.refresh(todo)

        return todo

    async def update(self, todo: Todo, todo_in: TodoUpdate) -> Todo:
        """Обновляет данные заметки."""
        # Обновляем поля заметки
        for field, value in todo_in.model_dump(exclude_unset=True).items():
            setattr(todo, field, value)

        # Сохраняем изменения в БД
        await self.db.commit()
        await self.db.refresh(todo)

        return todo

    async def delete(self, todo: Todo) -> None:
        """Удаляет заметку."""
        await self.db.delete(todo)
        await self.db.commit()
