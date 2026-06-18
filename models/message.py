
from datetime import datetime

from . import db


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    conversation_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "conversations.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False
    )
    # user | assistant | system

    content = db.Column(
        db.Text,
        nullable=False
    )

    token_count = db.Column(
        db.Integer,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def __repr__(self):
        return (
            f"<Message {self.id}>"
        )

