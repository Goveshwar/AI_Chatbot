
from models import db

from models.conversation import (
    Conversation
)

from models.message import (
    Message
)


def create_conversation(
    user_id: int,
    title: str = "New Chat"
):

    conversation = Conversation(
        title=title,
        user_id=user_id
    )

    db.session.add(
        conversation
    )

    db.session.commit()

    return conversation


def rename_conversation(
    conversation,
    title
):

    conversation.title = title

    db.session.commit()

    return conversation


def delete_conversation(
    conversation
):

    db.session.delete(
        conversation
    )

    db.session.commit()


def save_message(
    conversation_id,
    role,
    content
):

    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content
    )

    db.session.add(message)

    db.session.commit()

    return message


def get_messages(
    conversation
):

    return (
        Message.query
        .filter_by(
            conversation_id=conversation.id
        )
        .order_by(
            Message.created_at.asc()
        )
        .all()
    )


def build_conversation_context(
    conversation,
    max_messages=20
):

    messages = (
        Message.query
        .filter_by(
            conversation_id=conversation.id
        )
        .order_by(
            Message.created_at.desc()
        )
        .limit(max_messages)
        .all()
    )

    messages.reverse()

    context = []

    for message in messages:

        role = (
            "User"
            if message.role == "user"
            else "Assistant"
        )

        context.append(
            f"{role}: {message.content}"
        )

    return "\n".join(
        context
    )



