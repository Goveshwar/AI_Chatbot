
from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    EmailField,
    PasswordField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
    Regexp
)


class SignupForm(FlaskForm):

    name = StringField(
        "Full Name",
        validators=[
            DataRequired(),
            Length(
                min=2,
                max=100
            )
        ]
    )

    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(
                min=8,
                max=128
            ),

            Regexp(
                r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).+$",
                message=(
                    "Password must contain "
                    "uppercase, lowercase "
                    "and a number."
                )
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Passwords must match."
            )
        ]
    )

    submit = SubmitField(
        "Create Account"
    )

