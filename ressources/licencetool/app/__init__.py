from apiflask import APIFlask, Schema
from apiflask.fields import Integer, String
from apiflask.validators import Length, OneOf
from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = APIFlask(__name__, docs_path='/api/v1/docs')
    app.config.from_object(config_class)
    
    db.init_app(app)
    
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.licenses import bp as licenses_bp
    app.register_blueprint(licenses_bp, url_prefix='/api/v1/licenses')
    
    
    # Datenbank erstellen (nur beim ersten Start erforderlich)
    with app.app_context():
        db.create_all()
    
    return app