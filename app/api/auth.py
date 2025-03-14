from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import JWT_COOKIE_KEY, create_access_token
from app.schemas import Token
from app.services import UserService

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_service: UserService = Depends(),
) -> Any:
    """
    Аутентификация пользователя и получение JWT токена.

    - **username**: имя пользователя
    - **password**: пароль

    Возвращает JWT токен и устанавливает его в cookie.
    """

    # Аутентифицируем пользователя
    user = await user_service.authenticate(form_data.username, form_data.password)

    # Если пользователь не найден или пароль неверный, возвращаем ошибку
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
        )

    # Создаем JWT токен
    access_token = create_access_token(subject=user.id)

    # Устанавливаем JWT токен в cookie
    response.set_cookie(
        JWT_COOKIE_KEY, access_token, httponly=True, samesite="none", secure=True
    )

    return {"access_token": access_token}


@router.post("/logout")
async def logout(response: Response) -> Any:
    """
    Выход пользователя из системы.

    Удаляет JWT токен из cookie.
    """
    # Удаляем JWT токен из cookie
    response.delete_cookie(JWT_COOKIE_KEY)

    return {"detail": "Успешный выход из системы"}
