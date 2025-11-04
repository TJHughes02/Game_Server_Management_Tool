#file for utility functions
from app.models import GameServer, RconConfig, ServerInfo
from datetime import datetime, timezone

from app.routes import delete_server


def create_new_server(data):
    new_server = GameServer(
        name                = data.get("name"),
        game_type           = data.get("game_type"),
        status              = data.get("status", "Offline"),
        max_players         = data.get("maxPlayers", 1),
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
        start_at    = data.get("start_at", datetime.now(timezone.utc)),
        stopped_at  = data.get("stopped_at"),
        notes       = data.get("notes", "No notes at this time."),
    )
    return new_info