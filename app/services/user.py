from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.db import get_db
from app.models import User
from app.schemas import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_by_id(self, user_id: int) -> Optional[User]:
        """Получает пользователя по ID."""
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    async def get_by_username(self, username: str) -> Optional[User]:
        """Получает пользователя по имени пользователя."""
        result = await self.db.execute(select(User).filter(User.username == username))
        return result.scalars().first()

    async def create(self, user_in: UserCreate) -> User:
        """Создает нового пользователя."""
        # Создаем объект пользователя
        user = User(
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password),
        )

        # Добавляем пользователя в БД
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def update(self, user: User, user_in: UserUpdate) -> User:
        """Обновляет данные пользователя."""
        # Обновляем поля пользователя
        if user_in.username is not None:
            user.username = user_in.username
        if user_in.password is not None:
            user.hashed_password = get_password_hash(user_in.password)

        # Сохраняем изменения в БД
        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def delete(self, user: User) -> None:
        """Удаляет пользователя."""
        await self.db.delete(user)
        await self.db.commit()

    async def authenticate(self, username: str, password: str) -> Optional[User]:
        """Аутентифицирует пользователя."""
        # Получаем пользователя по имени пользователя
        user = await self.get_by_username(username)

        # Если пользователь не найден или пароль неверный, возвращаем None
        if not user or not verify_password(password, user.hashed_password):
            return None

        return user
