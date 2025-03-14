from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.core.security import JWT_COOKIE_KEY, get_current_user_id
from app.schemas import UserCreate, UserInfo, UserResponse, UserUpdate
from app.services import UserService

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    user_service: UserService = Depends(),
) -> Any:
    """
    Создание нового пользователя.

    - **username**: имя пользователя (уникальное)
    - **password**: пароль
    """
    # Проверяем, что пользователь с таким именем не существует
    user = await user_service.get_by_username(user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует",
        )

    # Создаем пользователя
    user = await user_service.create(user_in)

    return user


@router.get("/me", response_model=UserInfo)
async def get_current_user(
    user_service: UserService = Depends(),
    current_user_id: int = Depends(get_current_user_id),
) -> Any:
    """
    Получение информации о текущем пользователе.

    Возвращает информацию о текущем пользователе.
    """
    # Получаем пользователя по ID
    user = await user_service.get_by_id(current_user_id)

    # Если пользователь не найден, возвращаем ошибку
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    return user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_in: UserUpdate,
    user_service: UserService = Depends(),
    current_user_id: int = Depends(get_current_user_id),
) -> Any:
    """
    Обновление информации о текущем пользователе.

    - **username**: имя пользователя (уникальное)
    - **password**: пароль
    """
    # Получаем пользователя по ID
    user = await user_service.get_by_id(current_user_id)

    # Если пользователь не найден, возвращаем ошибку
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    # Проверяем, что пользователь с таким именем не существует
    if user_in.username is not None and user_in.username != user.username:
        existing_user = await user_service.get_by_username(user_in.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Пользователь с таким именем уже существует",
            )

    # Обновляем пользователя
    user = await user_service.update(user, user_in)

    return user


@router.delete("/me")
async def delete_current_user(
    response: Response,
    user_service: UserService = Depends(),
    current_user_id: int = Depends(get_current_user_id),
) -> Any:
    """
    Удаление текущего пользователя.
    """
    # Получаем пользователя по ID
    user = await user_service.get_by_id(current_user_id)

    # Если пользователь не найден, возвращаем ошибку
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден",
        )

    response.delete_cookie(JWT_COOKIE_KEY)
    # Удаляем пользователя
    await user_service.delete(user)

    return {"detail": "Пользователь успешно удален"}
