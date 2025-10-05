from app import create_app, db
from app.models import GameServer

app = create_app()

"""
    Server Column info
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(120), nullable=False)
    game_type           = db.Column(db.String(120), nullable=False)
    status              = db.Column(db.Enum("Online", "Offline", "Updating", "Starting", "Stopping", name="server_status"), nullable=False)
    server_port         = db.Column(db.Integer, nullable=False)
    install_path        = db.Column(db.String(255), nullable=False)
    archive_path        = db.Column(db.String(255), nullable=True)
    backup_path         = db.Column(db.String(255), nullable=True)
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

    test_server2 = GameServer(
        name = "Island Base PVE",
        game_type = "Ark: Survival Evolved",
        status = "Online",
        server_port = 5678,
        install_path = "ArkServer/Install/Path/Here",
        archive_path = "ArkServer/Archive/Path/Here",
        backup_path = "ArkServer/Backup/Path/Here",
    )

    db.session.add_all([test_server1, test_server2])
    db.session.commit()
    print("The Omnissiah smiles upon the sacred circuits. Test servers sanctified and brought online by anointed Tech-Priest.")