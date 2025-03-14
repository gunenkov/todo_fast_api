from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import get_current_user_id
from app.schemas import TodoCreate, TodoResponse, TodoUpdate
from app.services import TodoService

router = APIRouter()


@router.get("/", response_model=List[TodoResponse])
async def get_todos(
    skip: int = 0,
    limit: int = 100,
    todo_service: TodoService = Depends(),
    current_user_id: int = Depends(get_current_user_id),
) -> Any:
    """
    Получение списка заметок текущего пользователя.

    - **skip**: количество пропускаемых заметок (для пагинации)
    - **limit**: максимальное количество возвращаемых заметок (для пагинации)
    """

    # Получаем заметки пользователя с пагинацией
    todos = await todo_service.get_by_user_id(current_user_id, skip, limit)

    return todos


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
async def create_todo(
    todo_in: TodoCreate,
    todo_service: TodoService = Depends(),
    current_user_id: int = Depends(get_current_user_id),
) -> Any:
    """
    Создание новой заметки.

    - **title**: заголовок заметки
    - **description**: описание заметки (опционально)
    - **is_completed**: завершена ли заметка
    """
    # Создаем заметку
    todo = await todo_service.create(todo_in, current_user_id)

    return todo


@router.get("/{todo_id}", response_model=TodoResponse)
async def get_todo(
    todo_id: int,
    todo_service: TodoService = Depends(),
    current_user_id: int = Depends(get_current_user_id),
) -> Any:
    """
    Получение заметки по ID.

    - **todo_id**: ID заметки
    """
    # Получаем заметку по ID
    todo = await todo_service.get_by_id(todo_id)

    # Если заметка не найдена, возвращаем ошибку
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заметка не найдена",
        )

    # Проверяем, что заметка принадлежит текущему пользователю
    if todo.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этой заметке",
        )

    return todo


@router.put("/{todo_id}", response_model=TodoResponse)
async def update_todo(
    todo_id: int,
    todo_in: TodoUpdate,
    todo_service: TodoService = Depends(),
    current_user_id: int = Depends(get_current_user_id),
) -> Any:
    """
    Обновление заметки.

    - **todo_id**: ID заметки
    - **title**: заголовок заметки
    - **description**: описание заметки (опционально)
    - **is_completed**: завершена ли заметка
    """
    # Получаем заметку по ID
    todo = await todo_service.get_by_id(todo_id)

    # Если заметка не найдена, возвращаем ошибку
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заметка не найдена",
        )

    # Проверяем, что заметка принадлежит текущему пользователю
    if todo.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этой заметке",
        )

    # Обновляем заметку
    todo = await todo_service.update(todo, todo_in)

    return todo


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int,
    todo_service: TodoService = Depends(),
    current_user_id: int = Depends(get_current_user_id),
) -> Any:
    """
    Удаление заметки.

    - **todo_id**: ID заметки
    """
    # Получаем заметку по ID
    todo = await todo_service.get_by_id(todo_id)

    # Если заметка не найдена, возвращаем ошибку
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заметка не найдена",
        )

    # Проверяем, что заметка принадлежит текущему пользователю
    if todo.user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет доступа к этой заметке",
        )

    # Удаляем заметку
    await todo_service.delete(todo)

    return {"detail": "Заметка успешно удалена"}
