
# app.py

from flask import (
    Flask,
    render_template
)

from flask_login import (
    LoginManager
)

from flask_migrate import (
    Migrate
)

from config import Config
from models import db


login_manager = LoginManager()
migrate = Migrate()

login_manager.login_view = (
    "auth.login"
)

login_manager.login_message_category = (
    "warning"
)


def create_app():

    app = Flask(__name__)

    app.config.from_object(
        Config
    )

    # =====================
    # Extensions
    # =====================

    db.init_app(app)

    migrate.init_app(
        app,
        db
    )

    login_manager.init_app(
        app
    )

    # =====================
    # Import Models
    # =====================

    from models.user import User

    # =====================
    # User Loader
    # =====================

    @login_manager.user_loader
    def load_user(
        user_id
    ):

        try:

            return User.query.get(
                int(user_id)
            )

        except Exception:

            return None

    # =====================
    # Blueprints
    # =====================

    from routes.auth import (
        auth_bp
    )

    from routes.chat import (
        chat_bp
    )

    from routes.profile import (
        profile_bp
    )

    from routes.api import (
        api_bp
    )

    from routes.upload import (
        upload_bp
    )

    app.register_blueprint(
        auth_bp
    )

    app.register_blueprint(
        chat_bp
    )

    app.register_blueprint(
        profile_bp
    )

    app.register_blueprint(
        api_bp
    )

    app.register_blueprint(
        upload_bp
    )

    # =====================
    # Error Handlers
    # =====================

    @app.errorhandler(404)
    def not_found(error):

        return (
            render_template(
                "errors/404.html"
            ),
            404
        )

    @app.errorhandler(500)
    def internal_error(error):

        db.session.rollback()

        return (
            render_template(
                "errors/500.html"
            ),
            500
        )

    # =====================
    # Create Tables
    # =====================

    with app.app_context():

        db.create_all()

    return app


# =====================
# App Instance
# =====================

app = create_app()


# =====================
# Run Server
# =====================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )

