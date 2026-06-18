
from models.conversation import (
    Conversation
)

from models.message import (
    Message
)


def test_create_conversation(
    app,
    test_user
):

    with app.app_context():

        conversation = Conversation(
            title="Test Chat",
            user_id=test_user.id
        )

        from models import db

        db.session.add(
            conversation
        )

        db.session.commit()

        assert (
            conversation.id
            is not None
        )


def test_add_message(
    app,
    test_conversation
):

    with app.app_context():

        message = Message(
            conversation_id=
            test_conversation.id,
            role="user",
            content="Hello"
        )

        from models import db

        db.session.add(
            message
        )

        db.session.commit()

        assert (
            message.id
            is not None
        )

