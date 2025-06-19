from test import client
from unittest.mock import patch


@patch("app.auth.routes.build_msal_app")
def test_login_redirect(mock_build, client):
    mock_app = mock_build.return_value
    mock_app.get_authorization_request_url.return_value = "https://login.microsoftonline.com/mockauth"
    response = client.get("/api/v1/auth/login")
    assert response.status_code == 302
    assert "login.microsoftonline.com" in response.headers["Location"]


@patch("app.auth.routes.build_msal_app")
def test_auth_callback_invalid_state(mock_build, client):
    with client.session_transaction() as sess:
        sess["state"] = "original"
    response = client.get("/api/v1/auth/callback?state=wrong")
    assert response.status_code == 400
    assert b"Ung\xc3\xbcltiger Login-Status" in response.data


@patch("app.auth.routes.build_msal_app")
def test_auth_callback_success(mock_build, client):
    mock_app = mock_build.return_value
    mock_app.acquire_token_by_authorization_code.return_value = {
        "id_token_claims": {
            "preferred_username": "user@example.com",
            "name": "Test User"
        }
    }
    with client.session_transaction() as sess:
        sess["state"] = "correct"
    response = client.get("/api/v1/auth/callback?state=correct&code=123")
    assert response.status_code == 302


@patch("app.auth.routes.build_msal_app")
def test_auth_callback_error(mock_build, client):
    mock_app = mock_build.return_value
    mock_app.acquire_token_by_authorization_code.side_effect = Exception("fail")
    with client.session_transaction() as sess:
        sess["state"] = "correct"
    response = client.get("/api/v1/auth/callback?state=correct&code=fail")
    assert response.status_code == 500


def test_logout(client):
    with client.session_transaction() as sess:
        sess["user"] = {"email": "user@example.com"}
    response = client.get("/api/v1/auth/logout")
    assert response.status_code == 302
    assert "login.microsoftonline.com" in response.headers["Location"]

