
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    current_user
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models import db
from models.user import User

from forms.login_form import LoginForm
from forms.signup_form import SignupForm


auth_bp = Blueprint(
    "auth",
    __name__
)


# ==========================
# SIGNUP
# ==========================

@auth_bp.route(
    "/signup",
    methods=["GET", "POST"]
)
def signup():

    if current_user.is_authenticated:
        return redirect(
            url_for("chat.home")
        )

    form = SignupForm()

    if form.validate_on_submit():

        name = form.name.data.strip()

        email = (
            form.email.data
            .strip()
            .lower()
        )

        password = form.password.data

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            flash(
                "Email already exists.",
                "danger"
            )

            return redirect(
                url_for("auth.signup")
            )

        user = User(
            name=name,
            email=email,
            password_hash=
            generate_password_hash(
                password
            )
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "Account created successfully.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    return render_template(
        "signup.html",
        form=form
    )


# ==========================
# LOGIN
# ==========================

@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:
        return redirect(
            url_for("chat.home")
        )

    form = LoginForm()

    if form.validate_on_submit():

        email = (
            form.email.data
            .strip()
            .lower()
        )

        password = (
            form.password.data
        )

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:

            flash(
                "Invalid credentials.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        if not check_password_hash(
            user.password_hash,
            password
        ):

            flash(
                "Invalid credentials.",
                "danger"
            )

            return redirect(
                url_for("auth.login")
            )

        login_user(
            user,
            remember=form.remember_me.data
        )

        flash(
            "Welcome back!",
            "success"
        )

        return redirect(
            url_for("chat.home")
        )

    return render_template(
        "login.html",
        form=form
    )


# ==========================
# LOGOUT
# ==========================

@auth_bp.route(
    "/logout",
    methods=["POST"]
)
def logout():

    logout_user()

    flash(
        "Logged out successfully.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )

