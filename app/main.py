import asyncio
import os
import shutil
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from app.api.routes import api_router
from app.core.config import settings


# utils functions
@repeat_every(seconds=86400, wait_first=True)
def delete_old_folder():
    current_time = time.time()
    for item in os.listdir(settings.UPLOAD_FOLDER):
        item_path = os.path.join(settings.UPLOAD_FOLDER, item)
        creation_time = os.path.getctime(item_path)
        age_seconds = current_time - creation_time
        if age_seconds >= 86400:
            shutil.rmtree(item_path)


@asynccontextmanager
async def startup(app: FastAPI):
    try:
        os.makedirs(settings.UPLOAD_FOLDER, exist_ok=True)
        await delete_old_folder()
        yield
    except asyncio.CancelledError:
        print("Coroutine was cancelled.")


app = FastAPI(title=settings.PROJECT_NAME, lifespan=startup)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(api_router, prefix=settings.ROOT_URL_PREFIX)
