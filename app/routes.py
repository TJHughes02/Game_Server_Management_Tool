from flask import Blueprint, jsonify, request
from . import db
from .models import User

bp = Blueprint("routes", __name__)

@bp.route('/')
def home():
    return "Machine Spirit Awakened"

@bp.route("/api/health")
def health_check():
    machine_status = "awake and vigilant"
    return jsonify({"Status": f'The Machine Spirit is {machine_status}'})

@bp.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("display_name")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return jsonify({"Status": f'The Machine Spirit is pleased, Login Successful. Praise the Omnissiah!'})
    return jsonify({"Status": f'The Machine Spirit is displeased, Login Failed.'}), 401
