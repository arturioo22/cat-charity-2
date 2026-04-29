from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import main_router
from app.core.config import settings
from app.core.db import engine
from app.models.base import QRKotBase


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Асинхронный менеджер контекста для управления циклом приложения."""
    async with engine.begin() as conn:
        await conn.run_sync(QRKotBase.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(main_router)
