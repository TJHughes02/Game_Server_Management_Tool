#file for utility functions
from app.models import GameServer, RconConfig, ServerInfo


def create_new_server(data):
    new_server = GameServer(
        display_name    =data.get("name"),
        game_type       =data.get("game"),
        server_port     =data.get("serverPort")
        #install_path    = data.get(),
        #archive_path    = data.get(),
        #backup_path     = data.get()
    )
    return new_server

def create_new_server_rcon_config(data):
    new_rcon = RconConfig(
        """
        server_host_name    = data.get(),
        rcon_host           = data.get(),
        rcon_pass_hash      = data.get(),
        rcon_port           = data.get(),
        java_path           = data.get(),
        steam_cmd_path      = data.get()
        """
    )
    return new_rcon

def create_new_server_info(data):
    new_info = ServerInfo(
        """
        start_at    = data.get()
        stopped_at  = data.get()
        notes       = data.get()
        """
    )
    return new_info