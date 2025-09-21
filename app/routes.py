from flask import Blueprint, jsonify

bp = Blueprint("routes", __name__)

@bp.route("/api/health")
def health_check():
    return jsonify({"status": "ok"})