import os
from pathlib import Path

from decouple import config as decouple_conf
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "QUPLOAD"
    ROOT_URL_PREFIX: str = f"/{PROJECT_NAME.lower()}"
    BASE_DIR: str = str(Path(__file__).resolve().parent.parent.parent)
    TEMPLATE_DIR: str = os.path.join(BASE_DIR, 'templates')
    MEDIA_DIR: str = os.path.join(BASE_DIR, 'media')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 43800

    UPLOAD_FOLDER: str = decouple_conf("UPLOAD_FOLDER")
    DOMAIN_NAME: str = decouple_conf("DOMAIN_NAME")

    # EMAIL_HOST: str = decouple_conf("EMAIL_HOST")
    # EMAIL_PORT: int = decouple_conf("EMAIL_PORT")
    # EMAIL_HOST_USER: str = decouple_conf("EMAIL_HOST_USER")
    # EMAIL_HOST_PASSWORD: str = decouple_conf("EMAIL_HOST_PASSWORD")
    # FROM_MAIL: str = decouple_conf("FROM_MAIL")
    # MAIL_DOMAIN: str = decouple_conf("MAIL_DOMAIN")

    # EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"


settings = Settings()
