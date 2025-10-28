from flask import Blueprint, jsonify, request, session
from . import db, utils
from .models import User, GameServer

bp = Blueprint("routes", __name__)

"""
@bp.route('/')
def home():
    return "Machine Spirit Awakened"
"""


@bp.route("/api/home", methods=['GET'])
def home():
    print("The Data Reliquary hums. The faithful approach to commune with the Machine Spirit.")
    return jsonify({"Status": "OK"}), 200



@bp.route("/api/health")
def health_check():
    print("Machine Spirit Awake and Vigilant... Awaiting Communion with Tech-Priest...")
    machine_status = "Awaiting Tech-Priest"
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
        print("Tech-Priest is not recognized...")
        print("Rite of Activation failed...")
        return jsonify({"Status": f'The Machine Spirit recoils. Credentials rejected..'}), 401

    print("Rite of Activation successful...")
    print(f'Welcome Tech-Priest {user}...')
    #return jsonify({"Status": f'The Machine Spirit is pleased, Login Successful. Praise the Omnissiah!'})

    #session.clear()
    session["uid"] = user.id
    return jsonify({
        "Status": "Login Successful",
        "user": {"id": user.id, "display_name": user.display_name}
    }), 200


@bp.route("/api/me", methods=["GET"])
def me():
    uid = session.get("uid")
    if not uid:
        return jsonify({"Authenticated": False}), 200
    user = User.query.get(uid)
    if not user:
        session.clear()
        return jsonify({"Authenticated": False}), 200
    return jsonify({
        "Authenticated": True,
        "user": {"id": user.id, "display_name": user.display_name}
    }), 200


@bp.route("/api/logout", methods=["POST"])
def logout():
    print("Communion with the Machine Spirit severed. All sacred rites concluded. User egress complete.", flush= True)
    session.clear()
    return jsonify({"Communion Ended": True}), 200


@bp.route("/api/servers", methods=["GET"])
def get_servers():
    if "uid" not in session:
        print("Unauthorized Access attempted. Machine Spirit denies communion.")
        return jsonify({"Status": "Unauthorized Access"}), 401

    print("The sacred cogs turn. All servers hum in obedience, ready for manipulation by the anointed.")
    servers = GameServer.query.all()
    return jsonify([s.to_dict() for s in servers]), 200

@bp.route("/api/servers", methods=["POST"])
def new_server():
    print("Begun awakening new server....")
    data = request.get_json()
    try:
        print("Server begins to coalesce!")
        newest_server = utils.create_new_server(data)
        print("Configurations begin to settle!")
        newest_server.rcon_config = utils.create_new_server_rcon_config(data)
        print("Datavaults begin to fill with knowledge undimmed!")
        newest_server.server_info = utils.create_new_server_info(data)
        print("The Machine Spirit now deems this servers sanctity...")
        db.session.add(newest_server)
        db.session.commit()
        print("The sacred cogs whirl. A new server awakens, brought forth by the anointed Tech-Priest and sanctified by "
              "the Machine Spirit.")
        return jsonify(newest_server.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()
        print("Heretical error: New server dissipates back into the ether!")
        return jsonify({"Error": "Server Creation Failed"}), 500