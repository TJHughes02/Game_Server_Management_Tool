from flask import Blueprint, jsonify, request, session
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


# LOGIN SESSION TRACKING FOR PERSISTENT LOGIN SESSIONS
@bp.route("/api/login", methods=["POST"])
def login():
    print("Rite of Activation begun...")

    data = request.get_json(silent=True) or {}
    ident = (data.get("display_name") or "").strip()
    pwd = data.get("password") or ""
    if not ident or not pwd:
        return jsonify({"Status": "Missing credentials"}), 400

    user = User.query.filter_by(display_name=ident).first()
    if not user or not user.check_password(pwd):
        return jsonify({"Status": f'The Machine Spirit is displeased, Login Failed.'}), 401
    #print("Rite of Activation failed...")

    print("Rite of Activation successful...")
    #return jsonify({"Status": f'The Machine Spirit is pleased, Login Successful. Praise the Omnissiah!'})

    session.clear()
    session["uid"] = user.id
    return jsonify({
        "Status": "Login Successful",
        "user": {"id": user.id, "display_name": user.display_name}
    }), 200


@bp.route("/api/me", methods=["GET"])
def me():
    uid = session.get("uid")
    if not uid:
        return jsonify({"authenticated": False}), 200
    user = User.query.get(uid)
    if not user:
        session.clear()
        return jsonify({"authenticated": False}), 200
    return jsonify({
        "authenticated": True,
        "user": {"id": user.id, "display_name": user.display_name}
    }), 200


@bp.route("/api/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"ok": True}), 200
