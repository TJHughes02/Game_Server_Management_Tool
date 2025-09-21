from flask import Flask
from flask_cors import CORS

def create_app():
    # create the flask app obj and enable CORS so frontend requests can succeed
    app = Flask(__name__)
    CORS(app)
    #import and register routes (API endpoints)
    from .routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app