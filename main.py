import os
import string
import random
from decouple import config
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:8000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = config("UPLOAD_FOLDER")
DOMAIN_NAME = config("DOMAIN_NAME")

os.makedirs(os.path.join(os.getcwd(), UPLOAD_FOLDER), exist_ok=True)


def generate_random_string():
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(5))


@app.post("/unique-name/")
async def generate_unique_name():
    existing_names = set(os.listdir(UPLOAD_FOLDER))
    while True:
        random_string = generate_random_string()
        if random_string not in existing_names:
            os.mkdir(os.path.join(os.getcwd(), UPLOAD_FOLDER, random_string))
            return {"unique_name": random_string}


@app.post("/files/")
async def upload_file(file: UploadFile = File(...), unique_name: str = Form(...)):
    file_path = os.path.join(os.getcwd(), UPLOAD_FOLDER, unique_name, file.filename)
    file_content = file.file.read()
    with open(file_path, "wb") as f:
        f.write(file_content)
    return {"message": "File uploaded successfully"}


@app.get("/files/")
async def list_files(unique_name: str):
    file_path = os.path.join(os.getcwd(), UPLOAD_FOLDER, unique_name)
    files = os.listdir(file_path)
    return {"files": files}
