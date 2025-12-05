from flask import Blueprint, jsonify, request, session
from . import db, utils
from .models import User, GameServer
from .utils import DEFAULT_COMMANDS
from rcon import Client
from mcrcon import MCRcon

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

        db.session.flush()
        utils.provision_server_files(newest_server)

        db.session.commit()
        print("The sacred cogs whirl. A new server awakens, brought forth by the anointed Tech-Priest and sanctified by "
              "the Machine Spirit.")
        return jsonify(newest_server.to_dict()), 201

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
               "started_at": server.server_info.started_at, "active_players": server.active_players, "max_players": server.max_players,
               "connection": {
                   "host":          server.rcon_config.rcon_host,
                   "serverPort":    server.server_port,
                   "rcon": {"port": server.rcon_config.rcon_port}
               }}
    return jsonify(display), 200

@bp.route("/api/servers/<int:server_id>/<string:action>", methods=["POST"])
def server_action(server_id, action):
    if action == "start":
        utils.start_server(server_id)
        print(f'The sacred levers shift. Steam and ley currents align. Server {server_id} stirs from slumber, blessed by the Omnissiah.')
        return jsonify({"Status": "Started"}), 200
    elif action == "stop":
        utils.stop_server(server_id)
        print(f'The cogwork slows. The spark fades as the essence of Server {server_id} recedes. The Machine Spirit hums farewell.')
        return jsonify({"Status": "Stopped"}), 200
    elif action == "restart":
        utils.restart_server(server_id)
        print(f'The Tech-Priest chants the rites of renewal. The essence of Server {server_id} is made anew by sacred circuits.')
        return jsonify({"Status": "Restarted"}), 200
    else:
        print("Unrecognized action requested, seek a Magos for assistance.")
        return jsonify({"Status": "Unrecognized action requested"}), 500

@bp.route("/api/servers/<int:server_id>", methods=["DELETE"])
def delete_server(server_id):
    print(f'Machine Spirit enraged and focusing its ire on server {server_id}...')
    server = GameServer.query.get(server_id)
    try:
        db.session.delete(server)
        db.session.commit()
        print(f'The Machine Spirits ire ebbs... Server {server_id} has been purged.')
        return jsonify({f'Server Deletion Successful.'}), 200
    except Exception as e:
        db.session.rollback()
        import traceback
        print(f"Heretical error: Server {server_id} persists...")
        traceback.print_exc()
        return jsonify({"Error": "Server Deletion Failed"}), 500

@bp.route("/api/servers/<int:server_id>/rcon", methods=["POST"])
def rcon_command(server_id):
    if "uid" not in session:
        return jsonify({"Error": "Unauthorized"}), 401

    data = request.get_json()
    command = data.get("command")

    if not command:
        print("COMMAND ISSUE")
        return jsonify({"Error": "No command provided"}), 500

    server = GameServer.query.get(server_id)
    if not server:
        print("SERVER ISSUE")
        return jsonify({"Error": "Server not found"}), 404

    if server.status != "Online":
        print("STATUS ISSUE")
        return jsonify({"Error": "Server not online"}), 500

    try:
        print("WE GET TO THE TRY")
        rcon = server.rcon_config
        with MCRcon("127.0.0.1", rcon.rcon_pass_hash, rcon.rcon_port) as client:
            print(f"WE GET TO THE CLIENT")
            output = client.command(command)
            return jsonify({"success": True,
                            "output": output
                            }), 200

    except Exception as e:
        return jsonify({"success": False,
                        "error ": str(e)
                        }), 500

@bp.get("/api/session")
def session_me():
    uid = session.get("uid")
    if not uid:
        return jsonify({"ok": True, "user": None}), 200
    u = User.query.get(uid)
    return jsonify({"ok": True, "user": {"id": u.id, "display_name": u.display_name}}), 200

"""
LOGS ROUTEs
"""

@bp.route("/api/servers/<int:server_id>/logs", methods=["GET"])
def server_logs(server_id):
    """
    Return the tail of the Minecraft latest.log for this server.

    Response shape:
    {
      "server_id": 1,
      "lines": [...],
      "message": "optional info / error text"
    }
    """
    if "uid" not in session:
        return jsonify({"Status": "Unauthorized Access"}), 401

    server = GameServer.query.get(server_id)
    if not server:
        return jsonify({"Error": "Server not found"}), 404

    game = (server.game_type or "").lower()
    if "minecraft" not in game:
        return jsonify({"Error": "Logs only supported for Minecraft servers right now."}), 400

    # Optional ?lines=300 query parameter
    try:
        max_lines = request.args.get("lines", default=200, type=int)
    except Exception:
        max_lines = 200

    try:
        # read current players stored in DB
        raw_players = server.active_players or ""

        lines = utils.read_latest_log_lines(server, max_lines=max_lines)

        for line in lines:

            # -------- PLAYER JOINED --------
            if "joined the game" in line:
                players = {p.strip() for p in raw_players.split("\n") if p.strip()}
                # extract name cleanly
                name = line[33:].split("joined the game")[0].strip()

                if name not in players:
                    players.add(name)
                    server.active_players = "\n".join(sorted(players))
                    db.session.commit()

            # -------- PLAYER LEFT --------
            elif "left the game" in line:
                players = {p.strip() for p in raw_players.split("\n") if p.strip()}
                print("PLAYER LEFT BRANCH CURRENT PLAYERS: ", players)
                name = line[33:].split("left the game")[0].strip()
                print("NAME BEING REMOVED",name)

                if name in players:
                    print("THIS MOTHERFUCKER left:", name)
                    players.remove(name)
                    print("players after being removed: ", players)
                    server.active_players = "\n".join(sorted(players))
                    print("SERVER ACTIVE PLAYERS AFTER REMOVAL: ", server.active_players)
                    db.session.commit()
        return jsonify({
            "server_id": server.id,
            "lines": lines,
            "message": ""
        }), 200

    except FileNotFoundError:
        return jsonify({
            "server_id": server.id,
            "lines": [],
            "message": "Log file not found yet (has the server started and written any logs?)."
        }), 200

    except OSError as e:
        # Some OS-level issue while reading
        return jsonify({
            "server_id": server.id,
            "lines": [],
            "message": f"Could not read log file: {e}"
        }), 500
