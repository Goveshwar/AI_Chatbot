
from flask_wtf import FlaskForm

from wtforms import (
    EmailField,
    PasswordField,
    BooleanField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length
)


class LoginForm(FlaskForm):

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
            )
        ]
    )

    remember_me = BooleanField(
        "Remember Me"
    )

    submit = SubmitField(
        "Login"
    )

