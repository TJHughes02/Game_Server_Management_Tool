import os
BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-change-me")  # set via env in prod (dont have .env yet)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or f"sqlite:///{os.path.join(BASEDIR,'app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SAMESITE = "Lax"    # "Strict" if you don't embed cross-site
    SESSION_COOKIE_SECURE = False       # TRUE IN PROD ONLY!!!! HTTPS!
