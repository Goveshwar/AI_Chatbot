
import pytest

from app import create_app

from models import db

from models.user import User

from models.conversation import (
    Conversation
)


@pytest.fixture
def app():

    app = create_app()

    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI":
        "sqlite:///:memory:"
    })

    with app.app_context():

        db.create_all()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):

    return app.test_client()


@pytest.fixture
def test_user(app):

    with app.app_context():

        user = User(
            name="Test User",
            email="user@test.com",
            password_hash="hashed"
        )

        db.session.add(user)
        db.session.commit()

        return user


@pytest.fixture
def test_conversation(
    app,
    test_user
):

    with app.app_context():

        conversation = Conversation(
            title="Test",
            user_id=test_user.id
        )

        db.session.add(
            conversation
        )

        db.session.commit()

        return conversation

