import pytest

from app import create_app
from app.extensions import db
from config import TestingConfig


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(TestingConfig)

    with app.app_context():
        db.create_all()

        try:
            yield app
        finally:
            db.session.remove()
            db.drop_all()
            db.engine.dispose()


@pytest.fixture
def client(app):
    return app.test_client()