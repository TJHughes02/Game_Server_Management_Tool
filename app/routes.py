from flask import Blueprint, jsonify, request
#from . import db
#from .models import User

bp = Blueprint("routes", __name__)

@bp.route('/')
def home():
    return "Machine Spirit Awakened"

@bp.route("/api/health")
def health_check():
    machine_status = "awake and vigilant"
    return jsonify({"Status": f'The Machine Spirit is {machine_status}'})

"""
@bp.route("/api/users", methods=["GET"])
def list_users():
    return ""
"""