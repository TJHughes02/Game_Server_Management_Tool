from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Make sure the core folders exist when the app starts (will create if not in utils)
    from .utils import ensure_base_dirs
    utils.ensure_base_dirs()

    # CORS for Vite (dev ONLY)
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    # Session cookies (dev ONLY)
    app.config.update(
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_DOMAIN="localhost",  # REQUIRED FOR PROXY
    )

    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)
    return app
