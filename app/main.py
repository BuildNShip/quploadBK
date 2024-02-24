import os
import string
import random
import time
import shutil
import asyncio
from decouple import config
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

UPLOAD_FOLDER = config("UPLOAD_FOLDER")
DOMAIN_NAME = config("DOMAIN_NAME")


# utils functions
def get_response(message, response, code, has_error) -> JSONResponse:

    return JSONResponse(
        content={
            "hasError": has_error,
            "statusCode": code,
            "message": message,
            "response": response,
        },
        status_code=code,
    )


@repeat_every(seconds=86400, wait_first=True)
def delete_old_folder():
    current_time = time.time()
    for item in os.listdir(UPLOAD_FOLDER):
        item_path = os.path.join(UPLOAD_FOLDER, item)
        creation_time = os.path.getctime(item_path)
        age_seconds = current_time - creation_time
        if age_seconds >= 86400:
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
            return get_response("successfull", random_string, 200, False)


@app.post("/qupload/files/")
async def upload_file(file: UploadFile = File(...), unique_name: str = Form(...)):
    if not os.path.isdir(os.path.join(os.getcwd(), UPLOAD_FOLDER, unique_name)):
        return get_response("Invalid unique name", None, 404, True)
    file_path = os.path.join(os.getcwd(), UPLOAD_FOLDER, unique_name, file.filename)
    file_content = file.file.read()
    with open(file_path, "wb") as f:
        f.write(file_content)
    return get_response("successfull", None, 200, False)


@app.get("/qupload/files/{unique_name}")
async def list_files(unique_name: str):
    if not os.path.isdir(os.path.join(os.getcwd(), UPLOAD_FOLDER, unique_name)):
        return get_response("Invalid unique name", None, 404, True)
    file_path = os.path.join(os.getcwd(), UPLOAD_FOLDER, unique_name)
    files = os.listdir(file_path)
    files = [f"{DOMAIN_NAME}/qupload-media/{unique_name}/{file}" for file in files]
    return get_response("successfull", files, 200, False)
