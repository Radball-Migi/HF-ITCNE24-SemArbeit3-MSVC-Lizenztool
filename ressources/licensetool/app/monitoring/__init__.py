from apiflask import APIBlueprint

bp = APIBlueprint('monitoring', __name__)

from app.monitoring import routes