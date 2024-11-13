from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import DevelopmentConfig, TestingConfig, ProductionConfig
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__,template_folder="../templates")
    env = os.getenv("FLASK_ENV", "production")
    if env == "development":
        app.config.from_object(DevelopmentConfig)
    elif env == "testing":
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(ProductionConfig)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "user.login"

    from api.routes.user_routes import user_bp
    from api.routes.view_routes import view_bp
    from api.routes.home_routes import home_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(view_bp)
    app.register_blueprint(home_bp)

    return app

# Minimal user_loader function to satisfy Flask-Login
@login_manager.user_loader
def load_user(user_id):
    from api.models.user import User  # Import inside the function
    return User.query.get(int(user_id))
