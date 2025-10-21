#file for utility functions
from app.models import GameServer


def create_new_server(data):
    new_server = GameServer(
        display_name    =data.get("name"),
        game_type       =data.get("game"),
        server_port     =data.get("serverPort"),

    )
    return new_server