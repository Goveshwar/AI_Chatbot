from flask import (
    Blueprint,
    jsonify,
    request,
    session
)

from flask_login import (
    login_required,
    current_user
)

from models import db

from models.conversation import (
    Conversation
)

from models.message import (
    Message
)

from services.gemini_service import (
    generate_ai_response,
    generate_chat_title
)

from services.conversation_service import (
    build_conversation_context
)

from services.file_ingestion_service import (
    ingest_file
)

from services.rag_service import (
    ask_rag
)

api_bp = Blueprint(
    "api",
    __name__,
    url_prefix="/api"
)


@api_bp.route("/health")
def health():

    return jsonify({

        "status": "ok",
        "service": "chatgpt-clone"

    })


@api_bp.route(
    "/chat",
    methods=["POST"]
)
@login_required
def chat():

    try:

        data = request.get_json() or {}

        message = (
            data.get(
                "message",
                ""
            ).strip()
        )

        conversation_id = data.get(
            "conversation_id"
        )

        if not message:

            return jsonify({

                "success": False,

                "error":
                "Message is required."

            }), 400

        # ======================
        # FIND CONVERSATION
        # ======================

        conversation = None

        if conversation_id:

            conversation = (
                Conversation.query
                .filter_by(
                    id=conversation_id,
                    user_id=current_user.id
                )
                .first()
            )

        # ======================
        # CREATE NEW CONVERSATION
        # ======================

        if not conversation:

            conversation = Conversation(

                title="New Chat",

                user_id=current_user.id

            )

            db.session.add(
                conversation
            )

            db.session.commit()

        # ======================
        # SAVE USER MESSAGE
        # ======================

        user_message = Message(

            conversation_id=
            conversation.id,

            role="user",

            content=message

        )

        db.session.add(
            user_message
        )

        db.session.commit()

        # ======================
        # GENERATE CHAT TITLE
        # ONLY FOR FIRST MESSAGE
        # ======================

        message_count = (
            Message.query
            .filter_by(
                conversation_id=conversation.id
            )
            .count()
        )

        if message_count == 1:

            conversation.title = (
                generate_chat_title(
                    message
                )
            )

            db.session.commit()

                    # ======================
        # CHECK RAG MODE
        # ======================

        uploaded_file = session.get(
            "uploaded_file"
        )

        indexed_file = session.get(
            "indexed_file"
        )

        ai_response = ""

        if uploaded_file:

            try:

                if (
                    indexed_file
                    !=
                    uploaded_file
                ):

                    ingest_file(
                        uploaded_file
                    )

                    session[
                        "indexed_file"
                    ] = uploaded_file

                ai_response = ask_rag(
                    message
                )

            except Exception as e:

                ai_response = (
                    f"Document search error:\n\n{str(e)}"
                )

        else:

            conversation_context = (
                build_conversation_context(
                    conversation
                )
            )

            ai_response = (
                generate_ai_response(
                    conversation_context
                )
            )

        # ======================
        # SAVE AI RESPONSE
        # ======================

        assistant_message = Message(

            conversation_id=
            conversation.id,

            role="assistant",

            content=ai_response

        )

        db.session.add(
            assistant_message
        )

        conversation.updated_at = (
            db.func.now()
        )

        db.session.commit()

                # ======================
        # RESPONSE
        # ======================

        return jsonify({

            "success": True,

            "conversation_id":
            conversation.id,

            "conversation_title":
            conversation.title,

            "user_message": {

                "id":
                user_message.id,

                "role":
                "user",

                "content":
                user_message.content

            },

            "assistant_message": {

                "id":
                assistant_message.id,

                "role":
                "assistant",

                "content":
                assistant_message.content

            }

        })

    except Exception as e:

        db.session.rollback()

        return jsonify({

            "success": False,

            "error":
            str(e)

        }), 500