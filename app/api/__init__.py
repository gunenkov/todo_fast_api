from fastapi import APIRouter

from app.api import auth, todos, users

api_router = APIRouter(prefix="/api")

# Подключаем роутеры
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(todos.router, prefix="/todos", tags=["todos"])

__all__ = ["api_router"]
