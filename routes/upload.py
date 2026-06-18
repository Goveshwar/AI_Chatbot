
import os
import uuid

from flask import (
    Blueprint,
    request,
    jsonify,
    session
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import (
    secure_filename
)

from services.file_ingestion_service import (
    ingest_file
)


upload_bp = Blueprint(
    "upload",
    __name__
)


ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "txt"
}


MAX_FILE_SIZE = (
    10 * 1024 * 1024
)  # 10 MB


def allowed_file(
    filename
):

    return (
        "." in filename
        and
        filename.rsplit(
            ".",
            1
        )[1].lower()
        in ALLOWED_EXTENSIONS
    )


@upload_bp.route(
    "/upload",
    methods=["POST"]
)
@login_required
def upload_file():

    try:

        if (
            "file"
            not in request.files
        ):

            return jsonify({

                "success": False,

                "error":
                "No file uploaded"

            }), 400

        file = request.files[
            "file"
        ]

        if (
            file.filename == ""
        ):

            return jsonify({

                "success": False,

                "error":
                "No file selected"

            }), 400

        if not allowed_file(
            file.filename
        ):

            return jsonify({

                "success": False,

                "error":
                "Only PDF, DOCX and TXT files are allowed"

            }), 400

        # ======================
        # FILE SIZE CHECK
        # ======================

        file.seek(
            0,
            os.SEEK_END
        )

        size = file.tell()

        file.seek(0)

        if (
            size >
            MAX_FILE_SIZE
        ):

            return jsonify({

                "success": False,

                "error":
                "File exceeds 10MB limit"

            }), 400

        # ======================
        # UNIQUE FILENAME
        # ======================

        original_name = (
            secure_filename(
                file.filename
            )
        )

        extension = (
            original_name
            .split(".")[-1]
            .lower()
        )

        unique_name = (
            f"{uuid.uuid4()}.{extension}"
        )

        folder = os.path.join(
            "uploads",
            str(
                current_user.id
            ),
            extension
        )

        os.makedirs(
            folder,
            exist_ok=True
        )

        filepath = os.path.join(
            folder,
            unique_name
        )

        # ======================
        # SAVE FILE
        # ======================

        file.save(
            filepath
        )

        # ======================
        # INDEX FILE
        # ======================

        try:

            ingest_file(
                filepath
            )

        except Exception as e:

            return jsonify({

                "success": False,

                "error":
                f"Indexing failed: {e}"

            }), 500

        # ======================
        # STORE SESSION
        # ======================

        session[
            "uploaded_file"
        ] = filepath

        session[
            "uploaded_filename"
        ] = original_name

        session.modified = True

        return jsonify({

            "success": True,

            "filename":
            original_name,

            "filepath":
            filepath,

            "message":
            f"{original_name} uploaded and indexed successfully"

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error":
            str(e)

        }), 500

