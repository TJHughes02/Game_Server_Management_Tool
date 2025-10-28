from datetime import datetime, timezone
from app import create_app, db
from app.models import GameServer, ServerInfo, RconConfig, User


app = create_app()


def create_servers():
    """
        GameServer Columns
        id                  = db.Column(db.Integer, primary_key=True)
        name                = db.Column(db.String(120), nullable=False)
        game_type           = db.Column(db.String(120), nullable=False)
        status              = db.Column(db.Enum("Online", "Offline", "Updating", "Starting", "Stopping", name="server_status"), nullable=False)
        max_players          = db.Column(db.Integer, default=1)
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
            name="Mock-Craft",
            game_type="Minecraft",
            status="Offline",
            max_players=12,
            server_port=1234,
            install_path="MinecraftServer/Install/Path/Here",
            archive_path="MinecraftServer/Archive/Path/Here",
            backup_path="MinecraftServer/Backup/Path/Here",
        )

        test_server1.rcon_config = RconConfig(
            server_host_name="localhost_Minecraft",
            rcon_host="localhost_Minecraft",
            rcon_user="admin",
            rcon_pass_hash="",
            rcon_port=1234,
            java_path="java/path/here/Minecraft",
            steam_cmd_path="steam/path/here/Minecraft",
        )

        test_server1.server_info = ServerInfo(
            start_at=datetime.now(timezone.utc),
            stopped_at=datetime.now(timezone.utc),
            notes="Initial Setup for Minecraft",
        )

        test_server2 = GameServer(
            name="Faux Island Base PVE",
            game_type="Ark: Survival Evolved",
            status="Online",
            max_players=20,
            server_port=5678,
            install_path="ArkServer/Install/Path/Here",
            archive_path="ArkServer/Archive/Path/Here",
            backup_path="ArkServer/Backup/Path/Here",
        )

        test_server2.rcon_config = RconConfig(
            server_host_name="localhost_Ark",
            rcon_host="localhost_Ark",
            rcon_user="admin",
            rcon_pass_hash="",
            rcon_port=5678,
            java_path="java/path/here/Ark",
            steam_cmd_path="steam/path/here/Ark",
        )

        test_server2.server_info = ServerInfo(
            start_at=datetime.now(timezone.utc),
            stopped_at=datetime.now(timezone.utc),
            notes="Initial Setup for Ark"
        )

        db.session.add_all([test_server1, test_server2])
        db.session.commit()
        print("The Omnissiah smiles upon the sacred circuits. Test servers sanctified and brought online by "
              "anointed Tech-Priest.")

def create_user():
    with app.app_context():
        test_user = User(
            display_name="TestUser",
            email="testuser@gmail.com",
            # password = "password123",
            is_owner=False
        )
        test_user.set_pass("password123")
        db.session.add(test_user)
        db.session.commit()
        print("The Machine Spirit hums in solemn approval, Tech-Priest anointed. Praise the Omnissiah!")

def reset_db():
    with app.app_context():
        db.drop_all()
        db.create_all()
        create_user()
        create_servers()
        print("DATABASE RESET COMPLETE — The holy datavaults have been purged and rebuilt.\n"
                "User records initialized.\n"
                "Test servers sanctified.\n"
                "Machine Spirit reports full operational readiness.\n"
                "Praise the Omnissiah!")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "reset_db":
        reset_db()
    else:
        print("Usage: python test_db_manager.py reset_db")