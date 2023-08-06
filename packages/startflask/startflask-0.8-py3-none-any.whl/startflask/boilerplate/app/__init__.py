from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


def create_app():
    app = Flask(__name__)
    if os.environ.get('ENV') == 'production':
        app.config.from_object('app.config.ProductionConfig')
    else:
        app.config.from_object('app.config.Config')
    
    from app.models import db
    db.init_app(app)

    from app.auth import auth
    app.register_blueprint(auth.bp)
    from app.main import main
    app.register_blueprint(main.bp)

    return app