from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.core.config import api_config, cors_config
from app.db import create_tables


@asynccontextmanager
async def lifespan(_: FastAPI):
    await create_tables()
    yield


# Создаем экземпляр FastAPI
app = FastAPI(
    lifespan=lifespan,
    title=api_config.title,
    version=api_config.version,
    description=api_config.description,
    contact={
        "name": api_config.contact_name,
        "url": api_config.contact_url,
        "email": api_config.contact_email,
    },
)

# Добавляем middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_config.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем API роутеры
app.include_router(api_router)
