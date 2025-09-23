from flask import Blueprint, jsonify, request
from . import db
from .models import User

bp = Blueprint("routes", __name__)

"""
@bp.route('/')
def home():
    return "Machine Spirit Awakened"
"""

@bp.route("/api/health")
def health_check():
    print("Machine Spirit awaiting communion...")
    machine_status = "awaiting communion"
    return jsonify({"Status": f'The Machine Spirit is {machine_status}'})

@bp.route("/api/login", methods=["POST"])
def login():
    print("Rite of Activation begun...")
    data = request.json
    username = data.get("display_name")
    password = data.get("password")
    user = User.query.filter_by(display_name=username).first()
    if user and user.check_password(password):
        print("Rite of Activation successful...")
        return jsonify({"Status": f'The Machine Spirit is pleased, Login Successful. Praise the Omnissiah!'})
    print("Rite of Activation failed...")
    return jsonify({"Status": f'The Machine Spirit is displeased, Login Failed.'}), 401