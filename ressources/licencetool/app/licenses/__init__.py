from apiflask import APIBlueprint

bp = APIBlueprint('licenses', __name__)

from app.licenses import routes