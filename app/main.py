import os
import string
import random
import time
import shutil
import asyncio
from decouple import config
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

UPLOAD_FOLDER = config("UPLOAD_FOLDER")
DOMAIN_NAME = config("DOMAIN_NAME")


@repeat_every(seconds=86400, wait_first=True)
def delete_old_folder():
    current_time = time.time()
    for item in os.listdir(UPLOAD_FOLDER):
        item_path = os.path.join(UPLOAD_FOLDER, item)
        creation_time = os.path.getctime(item_path)
        age_seconds = current_time - creation_time
        if age_seconds >= 86400:
            print(f"Deleting {item_path}")
            shutil.rmtree(item_path)


@asynccontextmanager
async def startup(app: FastAPI):
    try:
        await delete_old_folder()
        yield
    except asyncio.CancelledError:
        print("Coroutine was cancelled.")


app = FastAPI(lifespan=startup)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


os.makedirs(os.path.join(os.getcwd(), UPLOAD_FOLDER), exist_ok=True)


def generate_random_string():
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(5))


@app.post("/qupload/get-unique-name/")
async def generate_unique_name():
    existing_names = set(os.listdir(UPLOAD_FOLDER))
    while True:
        random_string = generate_random_string()
        if random_string not in existing_names:
            os.mkdir(os.path.join(os.getcwd(), UPLOAD_FOLDER, random_string))
            return {"unique_name": random_string}


@app.post("/qupload/files/")
async def upload_file(file: UploadFile = File(...), unique_name: str = Form(...)):
    file_path = os.path.join(os.getcwd(), UPLOAD_FOLDER, unique_name, file.filename)
    file_content = file.file.read()
    with open(file_path, "wb") as f:
        f.write(file_content)
    return {"message": "File uploaded successfully"}


@app.get("/qupload/files/")
async def list_files(unique_name: str):
    file_path = os.path.join(os.getcwd(), UPLOAD_FOLDER, unique_name)
    files = os.listdir(file_path)
    return {"files": files}
