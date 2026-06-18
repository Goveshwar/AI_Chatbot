
from datetime import datetime

from . import db


class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(255),
        nullable=False,
        default="New Chat"
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    messages = db.relationship(
        "Message",
        backref="conversation",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Message.created_at.asc()"
    )

    def __repr__(self):
        return (
            f"<Conversation {self.id}>"
        )

