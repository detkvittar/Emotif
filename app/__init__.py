from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from flask_migrate import Migrate
from app.services.auth import auth
from app.api.routes import api
from app.data.database import db
from app.data.models import User, Post, Comment, Reaction  # Import models here

migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(api, url_prefix='/api')

    # Import models to ensure they're recognized damnit
    from app.data.models import User, Post, Comment, Reaction, Friendship, FollowRequest, ViewedPost, Notification, \
        Block

    with app.app_context():
        db.create_all()

    return app
