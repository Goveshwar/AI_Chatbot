
from models.user import User

from models.conversation import (
    Conversation
)

from models.message import (
    Message
)


def test_user_model(app):

    with app.app_context():

        user = User(
            name="Goveshwar",
            email="gov@test.com",
            password_hash="hashed"
        )

        assert (
            user.name ==
            "Goveshwar"
        )

        assert (
            user.email ==
            "gov@test.com"
        )


def test_conversation_model(
    app
):

    with app.app_context():

        conversation = Conversation(
            title="Python"
        )

        assert (
            conversation.title ==
            "Python"
        )


def test_message_model(
    app
):

    with app.app_context():

        message = Message(
            role="assistant",
            content="Hello"
        )

        assert (
            message.role ==
            "assistant"
        )

        assert (
            message.content ==
            "Hello"
        )

