from flask import Flask
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from .config import Config
from app.models import db
from .routes.auth import auth_bp
from app.routes.note import note_bp
from app.routes.tag import tag_bp
from app.routes.user import user_bp

jwt = JWTManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = Config.SECRET_KEY
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = Config.JWT_ACCESS_TOKEN_EXPIRES


    app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_URL
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    


    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(note_bp, url_prefix="/api/note")
    app.register_blueprint(tag_bp, url_prefix="/api/tag")
    app.register_blueprint(user_bp, url_prefix="/api/user")

    return app