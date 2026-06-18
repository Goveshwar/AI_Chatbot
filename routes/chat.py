from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_required,
    current_user
)

from models import db
from models.conversation import Conversation

chat_bp = Blueprint(
    "chat",
    __name__
)


# ====================================
# HOME
# ====================================

@chat_bp.route("/")
@login_required
def home():

    conversations = (
        Conversation.query
        .filter_by(
            user_id=current_user.id
        )
        .order_by(
            Conversation.updated_at.desc()
        )
        .all()
    )

    return render_template(
        "chat/index.html",
        conversations=conversations,
        active_conversation=None
    )


# ====================================
# NEW CHAT
# ====================================

@chat_bp.route("/new-chat")
@login_required
def new_chat():

    return redirect(
        url_for("chat.home")
    )


# ====================================
# OPEN CHAT
# ====================================

@chat_bp.route(
    "/conversation/<int:conversation_id>"
)
@login_required
def conversation(
    conversation_id
):

    active_conversation = (
        Conversation.query
        .filter_by(
            id=conversation_id,
            user_id=current_user.id
        )
        .first_or_404()
    )

    conversations = (
        Conversation.query
        .filter_by(
            user_id=current_user.id
        )
        .order_by(
            Conversation.updated_at.desc()
        )
        .all()
    )

    return render_template(
        "chat/index.html",
        conversations=conversations,
        active_conversation=active_conversation
    )


# ====================================
# DELETE CHAT
# ====================================

@chat_bp.route(
    "/conversation/<int:conversation_id>/delete",
    methods=["POST"]
)
@login_required
def delete_conversation(
    conversation_id
):

    conversation = (
        Conversation.query
        .filter_by(
            id=conversation_id,
            user_id=current_user.id
        )
        .first_or_404()
    )

    db.session.delete(
        conversation
    )

    db.session.commit()

    flash(
        "Conversation deleted successfully.",
        "success"
    )

    return redirect(
        url_for("chat.home")
    )