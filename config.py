import os
from aws_secrets import get_database_url


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")

    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY environment variable is required")

    SQLALCHEMY_DATABASE_URI = (
            os.getenv("DATABASE_URL")
            or get_database_url()
            or "sqlite:///tutorflow.db"
    )


    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test-secret-key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"