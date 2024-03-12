import os

from fastapi import APIRouter
from fastapi import UploadFile, File, Form

from app.core.config import settings
from app.util.general import generate_random_string
from app.util.response import CustomResponse

router = APIRouter()


@router.post("/get-unique-name/")
async def generate_unique_name():
    existing_names = set(os.listdir(settings.UPLOAD_FOLDER))
    while True:
        random_string = generate_random_string()
        if random_string not in existing_names:
            os.mkdir(os.path.join(settings.UPLOAD_FOLDER, random_string))
            return CustomResponse(response={'unique_code': random_string}).get_success_response()


@router.post("/files/")
async def upload_file(file: UploadFile = File(...), unique_name: str = Form(...)):
    if not os.path.isdir(os.path.join(os.getcwd(), settings.UPLOAD_FOLDER, unique_name)):
        return CustomResponse(general_message="Invalid unique name").get_failure_response()
    file_path = os.path.join(os.getcwd(), settings.UPLOAD_FOLDER, unique_name, file.filename)
    file_content = file.file.read()
    with open(file_path, "wb") as f:
        f.write(file_content)
    return CustomResponse(general_message="File uploaded successfully").get_success_response()


@router.get("/files/{unique_name}")
async def list_files(unique_name: str):
    if not os.path.isdir(os.path.join(os.getcwd(), settings.UPLOAD_FOLDER, unique_name)):
        return CustomResponse(general_message="Invalid unique name").get_failure_response()
    file_path = os.path.join(os.getcwd(), settings.UPLOAD_FOLDER, unique_name)
    files = os.listdir(file_path)
    files = [f"{settings.DOMAIN_NAME}/qupload-media/{unique_name}/{file}" for file in files]
    return CustomResponse(response={'files': files}).get_success_response()
