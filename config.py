import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" +
        os.path.join(
            BASE_DIR,
            "database",
            "chatbot.db"
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GEMINI_API_KEY = os.getenv(
        "GEMINI_API_KEY"
    )

    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"