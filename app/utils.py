#file for utility functions
from app.models import GameServer, RconConfig, ServerInfo
from app import db
from datetime import datetime, timezone
import time


DEFAULT_COMMANDS = {
    "Minecraft (Java Edition)": {
        "broadcast":    "/say {message}",
        "list_players": "/list",
        "kick":         "/kick {player}",
        "ban":          "/ban {player}",
        "unban":        "/pardon {player}",
        "save":         "/save-all"
    },
    "ARK: Survival Evolved": {
        "broadcast":    "ServerChat {message}",
        "list_players": "ListPlayers",
        "kick":         "KickPlayer {steamid}",
        "ban":          "BanPlayer {steamid}",
        "unban":        "UnbanPlayer {steamid}",
        "save":         "SaveWorld"
    },
    "Rust":{
        "broadcast":    "say {message}",
        "list_players": "playerlist",
        "kick":         "kick {player}",
        "ban":          "ban {player}",
        "unban":        "unban {player}",
        "save":         "server.save"
    },
    "Counter-Strike: Global Offensive": {
        "broadcast":    "say {message}",
        "list_players": "status",
        "kick":         "kick {player}",
        "ban":          "banid {steamid}",
        "unban":        "removeid {steamid}",
        "save":         "host_writeconfig"
    },
    "Factorio": {
        "broadcast":    "/c game.print(\"{message}\")",
        "list_players": "/c for _, player in pairs(game.connected_players) do game.print(player.name) end",
        "kick":         "/c game.players[\"{player}\"].ban(\"You have been kicked\")",
        "ban":          "/c game.players[\"{player}\"].ban(\"Banned\")",
        "unban":        "/c game.players[\"{player}\"].unban()",
        "save":         "/c game.server_save()"
    },
    # more games/commands to be added later?
}

def create_new_server(data):
    new_server = GameServer(
        name                = data.get("name"),
        game_type           = data.get("game_type"),
        status              = data.get("status", "Offline"),
        max_players         = int(data.get("extras", {}).get("maxPlayers", 0)),
        server_port         = data.get("server_port"),
        install_path        = data.get("install_path"),
        archive_path        = data.get("archive_path", None),
        backup_path         = data.get("back_up_path", None),
    )
    return new_server

def create_new_server_rcon_config(data):
    new_rcon = RconConfig(
        server_host_name    = data.get("server_host_name"),
        rcon_host           = data.get("rcon_host"),
        rcon_user           = data.get("rcon_user"),
        rcon_pass_hash      = data.get("rcon_pass_hash"),
        rcon_port           = data.get("rcon_port"),
        java_path           = data.get("java_path"),
        steam_cmd_path      = data.get("steam_cmd_path")
    )
    return new_rcon

def create_new_server_info(data):
    new_info = ServerInfo(
        notes       = data.get("notes", "No notes at this time."),
    )
    return new_info

def start_server(server_id):
    server = GameServer.query.get(server_id)
    server.status = "Starting"
    db.session.commit()
    # code to start the game server
    time.sleep(5) #simulate transition
    # verify server started, then set status
    server.server_info.started_at = datetime.now(timezone.utc)
    server.status = "Online"
    db.session.commit()

def stop_server(server_id):
    server = GameServer.query.get(server_id)
    server.status = "Stopping"
    db.session.commit()
    # code to stop the server
    time.sleep(5) #simulate transition
    # verify server stopped and resources freed, then set status
    server.server_info.stopped_at = datetime.now(timezone.utc)
    server.status = "Offline"
    db.session.commit()

def restart_server(server_id):
    stop_server(server_id)
    time.sleep(5) #simulate transition
    start_server(server_id)
    db.session.commit()

def update_server(server_id):
    server = GameServer.query.get(server_id)
    server.status = "Updating"
    # code for updating the server
    db.session.commit()
