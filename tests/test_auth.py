
from models.user import User


def test_signup(client, app):

    response = client.post(
        "/signup",
        data={
            "name": "Goveshwar",
            "email": "test@test.com",
            "password": "Password123",
            "confirm_password": "Password123"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():

        user = User.query.filter_by(
            email="test@test.com"
        ).first()

        assert user is not None


def test_login(client, app):

    response = client.post(
        "/login",
        data={
            "email": "test@test.com",
            "password": "Password123"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

