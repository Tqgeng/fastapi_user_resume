from contextlib import asynccontextmanager
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.api_v1 import pages
from core.config import settings
from core.models import db_helper

from api import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

main_app = FastAPI(lifespan=lifespan)
main_app.include_router(api_router)
main_app.include_router(pages.router)

main_app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


if __name__ == "__main__":
    uvicorn.run(
        "main:main_app",
        port=settings.run.port,
        host=settings.run.host,
        reload=True,
    )
