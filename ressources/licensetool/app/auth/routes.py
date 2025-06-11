from app.auth import bp
from flask import session, redirect, request, url_for, current_app
from msal import ConfidentialClientApplication
import uuid

# --- Globale Werte ---
REDIRECT_PATH = "callback"
SCOPE = []

def build_msal_app():
    client_id = current_app.config["CLIENT_ID"]
    client_secret = current_app.config["CLIENT_SECRET"]
    tenant_id = current_app.config["TENANT_ID"]
    authority = f"https://login.microsoftonline.com/{tenant_id}"
    secret_key = current_app.config["SECRET_KEY"]

    return ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret,
    )

# --- Login-Route ---
@bp.route("/login")
def login():
    session["state"] = str(uuid.uuid4())
    msal_app = build_msal_app()
    auth_url = msal_app.get_authorization_request_url(
        scopes=SCOPE,
        state=session["state"],
        redirect_uri=url_for("auth.auth_callback", _external=True),
    )
    return redirect(auth_url)

# --- Callback-Route nach Microsoft-Login ---
@bp.route(REDIRECT_PATH)
def auth_callback():
    if request.args.get("state") != session.get("state"):
        return "Ungültiger Login-Status (State mismatch)", 400

    code = request.args.get("code")
    msal_app = build_msal_app()
    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=SCOPE,
        redirect_uri=url_for("auth.auth_callback", _external=True),
    )

    if "id_token_claims" in result:
        session["user"] = {
            "name": result["id_token_claims"].get("name"),
            "email": result["id_token_claims"].get("preferred_username"),
        }
        return redirect(url_for("main.show_frontend"))  # ggf. anpassen
    else:
        return f"Fehler beim Authentifizieren: {result.get('error_description', 'Unbekannter Fehler')}", 401

# --- Logout-Route ---
@bp.route("/logout")
def logout():
    session.clear()
    return redirect(
        f"https://login.microsoftonline.com/common/oauth2/v2.0/logout"
        f"?post_logout_redirect_uri={url_for('main.show_frontend', _external=True)}"
    )
