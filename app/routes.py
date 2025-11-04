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

@bp.route("/api/servers/<int:server_id>", methods=["GET"])
def display_server(server_id):
    print(f'Beginning Hymn of Access to Server {server_id}...')
    if "uid" not in session:
        print("Unauthorized Access attempted. Machine Spirit denies communion.")
        return jsonify({"Status": "Unauthorized Access"}), 401
    print(f'Hymn of Access complete, communion with server {server_id} begun...')
    server = GameServer.query.get(server_id)
    display = {"id": server.id, "name": server.name, "game": server.game_type, "status": (server.status or "").lower(),
               "connection": {
                   "host": server.rcon_config.rcon_host,
                   "serverPort": server.server_port,
                   "rcon": {"port": server.rcon_config.rcon_port},
               }}
    return jsonify(display), 200

@bp.route("/api/servers/<int:server_id>/<string:action>", methods=["POST"])
def server_action(server_id, action):
    if action == "start":
        print(f'The sacred levers shift. Steam and ley currents align. Server {server_id} stirs from slumber, blessed by the Omnissiah.')
        return jsonify({"Status": "Started"}), 200
    elif action == "stop":
        print(f'The cogwork slows. The Sparks fade as the essence of Server {server_id} recedes. The Machine Spirit hums farewell.')
        return jsonify({"Status": "Stopped"}), 200
    elif action == "restart":
        print(f'The Tech-Priest chants the rites of renewal. The essence of Server {server_id} is remade anew by sacred circuits.')
        return jsonify({"Status": "Restarted"}), 200
    else:
        print("Unrecognized action requested, seek a Magos for assistance.")
        return jsonify({"Status": "Unrecognized action requested"}), 500

@bp.route("/api/servers/<int:server_id>", methods=["DELETE"])
def delete_server(server_id):
    print(f'Machine Spirit enraged and focusing its ire on server {server_id}...')
    try:
        db.session.query(GameServer).filter_by(id=server_id).delete()
        db.session.commit()
        print(f'The Machine Spirits ire ebbs... Server {server_id} has been purged.')
        return jsonify({f'Server Deletion Successful.'}), 200
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"Heretical error: {server_id} persists...")
        return jsonify({"Error": "Server Deletion Failed"}), 500