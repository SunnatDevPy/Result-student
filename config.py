import os
from dataclasses import dataclass, asdict
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()


@dataclass
class BaseConfig:
    def asdict(self):
        return asdict(self)


@dataclass
class DB_CONFIG(BaseConfig):
    DB_NAME: str = os.getenv('DB_NAME')
    DB_USER: str = os.getenv('DB_USER')
    DB_PASS: str = os.getenv('DB_PASS')
    DB_HOST: str = os.getenv('DB_HOST')
    DB_PORT: str = os.getenv('DB_PORT')

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@dataclass
class BOT(BaseConfig):
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    ADMIN = os.getenv('ADMIN')
    OWNER = os.getenv('OWNER')
    LIST = [int(ADMIN), int(OWNER)]
    PAYMENT = os.getenv('PAYMENT_TOKEN')
    ADMIN_PASS = os.getenv('ADMIN_PASS')
    ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')

    WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST")
    WEB_SERVER_PORT = int(os.getenv("WEB_SERVER_PORT"))

    WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
    WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")
    BASE_WEBHOOK_URL = os.getenv("BASE_WEBHOOK_URL")

@dataclass
class Config:
    db = DB_CONFIG()
    bot = BOT()


conf = Config
