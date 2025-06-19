from app.auth import bp
from flask import session, redirect, request, url_for, current_app
from msal import ConfidentialClientApplication
import uuid
import logging

# --- Globale Werte ---
REDIRECT_PATH = "callback"
SCOPE = []

# --- Logging initialisieren ---
logger = logging.getLogger(__name__)

def build_msal_app():
    client_id = current_app.config["CLIENT_ID"]
    client_secret = current_app.config["CLIENT_SECRET"]
    tenant_id = current_app.config["TENANT_ID"]
    authority = f"https://login.microsoftonline.com/{tenant_id}"

    return ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret,
    )

# --- Login-Route ---
@bp.route("/login")
def login():
    logger.info("Login-Route wurde aufgerufen")

    session["state"] = str(uuid.uuid4())
    msal_app = build_msal_app()
    auth_url = msal_app.get_authorization_request_url(
        scopes=SCOPE,
        state=session["state"],
        redirect_uri=url_for("auth.auth_callback", _external=True),
    )
    logger.debug(f"Weiterleitung zur Microsoft-Login-URL: {auth_url}")
    return redirect(auth_url)

# --- Callback-Route nach Microsoft-Login ---
@bp.route(REDIRECT_PATH)
def auth_callback():
    logger.info("Auth-Callback erreicht")

    if request.args.get("state") != session.get("state"):
        logger.warning("Ungültiger Login-Status (State mismatch)")
        return "Ungültiger Login-Status (State mismatch)", 400

    code = request.args.get("code")
    msal_app = build_msal_app()
    try:
        result = msal_app.acquire_token_by_authorization_code(
            code,
            scopes=SCOPE,
            redirect_uri=url_for("auth.auth_callback", _external=True),
        )
    except Exception as e:
        logger.exception("Fehler beim Abrufen des Tokens mit dem Autorisierungscode")
        return "Authentifizierungsfehler", 500

    if "id_token_claims" in result:
        user_email = result["id_token_claims"].get("preferred_username", "<unbekannt>")
        logger.info(f"Benutzer eingeloggt: {user_email}")
        session["user"] = {
            "name": result["id_token_claims"].get("name"),
            "email": user_email,
        }
        return redirect(url_for("main.show_frontend"))
    else:
        error_msg = result.get("error_description", "Unbekannter Fehler")
        logger.error(f"Fehler beim Authentifizieren: {error_msg}")
        return f"Fehler beim Authentifizieren: {error_msg}", 401

# --- Logout-Route ---
@bp.route("/logout")
def logout():
    user_email = session.get("user", {}).get("email", "<nicht angemeldet>")
    logger.info(f"Benutzer ausgeloggt: {user_email}")
    session.clear()
    return redirect(
        f"https://login.microsoftonline.com/common/oauth2/v2.0/logout"
        f"?post_logout_redirect_uri={url_for('main.show_frontend', _external=True)}"
    )

# --- Test-Login-Route für Tests ---
# Diese Route ist nur verfügbar, wenn die App im Testmodus läuft.
@bp.route('/test-login', methods=['POST'])
def test_login():
    if not current_app.config.get("TESTING", False):
        return {"error": "Not allowed"}, 403

    session["user"] = {
        "name": "Test User",
        "preferred_username": "test@example.com"
    }
    return {"message": "Logged in"}, 200