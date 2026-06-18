
from datetime import datetime

from flask_login import UserMixin

from . import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(255),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    is_active_user = db.Column(
        db.Boolean,
        default=True
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

    # Relationships

    conversations = db.relationship(
        "Conversation",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<User {self.email}>"
        )

