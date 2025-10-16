from datetime import datetime, timezone

from app import create_app, db
from app.models import GameServer, ServerInfo, RconConfig

app = create_app()

"""
    GameServer Columns
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(120), nullable=False)
    game_type           = db.Column(db.String(120), nullable=False)
    status              = db.Column(db.Enum("Online", "Offline", "Updating", "Starting", "Stopping", name="server_status"), nullable=False)
    server_port         = db.Column(db.Integer, nullable=False)
    install_path        = db.Column(db.String(255), nullable=False)
    archive_path        = db.Column(db.String(255), nullable=True)
    backup_path         = db.Column(db.String(255), nullable=True)

    Rcon Config Columns
    id                  = db.Column(db.Integer, db.ForeignKey('game_server.id'), primary_key=True)
    server_host_name    = db.Column(db.String(80), nullable=False)
    rcon_host           = db.Column(db.String(255), nullable=False)
    rcon_user           = db.Column(db.String(80), nullable=False)
    rcon_pass_hash      = db.Column(db.String(255), nullable=False)
    rcon_port           = db.Column(db.Integer, nullable=False)
    java_path           = db.Column(db.String(255), nullable=False)
    steam_cmd_path      = db.Column(db.String(255), nullable=False)

    Server Info Columns
    id                  = db.Column(db.Integer, db.ForeignKey("game_server.id"), primary_key = True)
    start_at            = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    stopped_at          = db.Column(db.DateTime, nullable=True)
    notes               = db.Column(db.Text, nullable=True)

"""

with app.app_context():
    test_server1 = GameServer(
        name = "Mock-Craft",
        game_type = "Minecraft",
        status = "Offline",
        server_port = 1234,
        install_path = "MinecraftServer/Install/Path/Here",
        archive_path = "MinecraftServer/Archive/Path/Here",
        backup_path = "MinecraftServer/Backup/Path/Here",
    )
    db.session.add(test_server1)
    db.session.flush()

    rcon1 = RconConfig(
        id = test_server1.id,
        server_host_name = "localhost_Minecraft",
        rcon_host = "localhost_Minecraft",
        rcon_pass_hash = "",
        rcon_port = 1234,
        java_path = "java/path/here/Minecraft",
        steam_cmd_path = "steam/path/here/Minecraft",
    )
    db.session.add(rcon1)

    info1 = ServerInfo(
        id = test_server1.id,
        start_at = datetime.now(timezone.utc),
        stopped_at = datetime.now(timezone.utc),
        notes = "Initial Setup for Minecraft",
    )
    db.session.add(info1)

    test_server2 = GameServer(
        name = "Island Base PVE",
        game_type = "Ark: Survival Evolved",
        status = "Online",
        server_port = 5678,
        install_path = "ArkServer/Install/Path/Here",
        archive_path = "ArkServer/Archive/Path/Here",
        backup_path = "ArkServer/Backup/Path/Here",
    )
    db.session.add(test_server2)
    db.session.flush()

    rcon2 = RconConfig(
        id = test_server2.id,
        server_host_name = "localhost_Ark",
        rcon_host = "localhost_Ark",
        rcon_pass_hash = "",
        rcon_port = 5678,
        java_path = "java/path/here/Ark",
        steam_cmd_path = "steam/path/here/Ark",
    )
    db.session.add(rcon2)

    info2 = ServerInfo(
        id = test_server2.id,
        start_at = datetime.now(timezone.utc),
        stopped_at = datetime.now(timezone.utc),
        notes = "Initial Setup for Ark"
    )
    db.session.add(info2)

    db.session.commit()
    print("The Omnissiah smiles upon the sacred circuits. Test servers sanctified and brought online by anointed Tech-Priest.")