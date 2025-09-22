from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy() #create ORM
migrate = Migrate()

def create_app():
    # create the flask app obj and enable CORS so frontend requests can succeed
    app = Flask(__name__)
    CORS(app, origins=["http://localhost:5173"])
    #configure flask app
    app.config.from_object(Config)

    #link database to Flask and enable migrations
    db.init_app(app)
    migrate.init_app(app, db)

    #import and register routes (API endpoints)
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app