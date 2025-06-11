from apiflask import APIBlueprint

bp = APIBlueprint('auth', __name__)

from app.auth import routes