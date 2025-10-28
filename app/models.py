from app import db
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

#relationship function set up == attribute_name = db.relationship("target_class_name", back_populates="attribute_name")

#User table
class  User(db.Model):
    __tablename__       = "user"
    id                  = db.Column(db.Integer, primary_key=True)
    email               = db.Column(db.String(255), unique=True, nullable=True)
    is_owner            = db.Column(db.Boolean)
    display_name        = db.Column(db.String(80), unique=True, nullable=False)
    pass_hash           = db.Column(db.String(255), nullable=False)

    game_servers = db.relationship("GameServerUser", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.id}; {self.display_name}>"

    def set_pass(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)

#Game Server User table
class GameServerUser(db.Model):
    __tablename__       = "game_server_user"
    user_id             = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    server_id           = db.Column(db.Integer, db.ForeignKey("game_server.id"), primary_key=True)
    role                = db.Column(db.String(50), nullable=False)

    user = db.relationship("User", back_populates="game_servers")
    servers = db.relationship("GameServer", back_populates="users")


#Servers table
class GameServer(db.Model):
    __tablename__       = "game_server"
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(120), nullable=False)
    game_type           = db.Column(db.String(120), nullable=False)
    status              = db.Column(db.Enum("Online", "Offline", "Updating", "Starting", "Stopping",
                                            name="server_status"), nullable=False, default="Offline")
    server_port         = db.Column(db.Integer, nullable=False)
    install_path        = db.Column(db.String(255), nullable=False)
    archive_path        = db.Column(db.String(255), nullable=True)
    backup_path         = db.Column(db.String(255), nullable=True)

    rcon_config = db.relationship("RconConfig", back_populates="server", uselist=False, cascade="all, delete-orphan")
    server_info = db.relationship("ServerInfo", back_populates="server", uselist=False, cascade="all, delete-orphan")

    users = db.relationship("GameServerUser", back_populates="servers", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<GameServer {self.id}; {self.name}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "game": self.game_type,
            "status": self.status,
            "players": 0,
            "uptimeSec": 0
        }

class RconConfig(db.Model):
    __tablename__       = "rcon_config"
    id                  = db.Column(db.Integer, db.ForeignKey("game_server.id"), primary_key=True)
    server_host_name    = db.Column(db.String(80), nullable=False)
    rcon_host           = db.Column(db.String(255), nullable=False)
    rcon_user           = db.Column(db.String(80), nullable=False)
    rcon_pass_hash      = db.Column(db.String(255), nullable=False)
    rcon_port           = db.Column(db.Integer, nullable=False)
    java_path           = db.Column(db.String(255), nullable=False)
    steam_cmd_path      = db.Column(db.String(255), nullable=False)

    server = db.relationship("GameServer", back_populates="rcon_config")

#Server Info table
class ServerInfo(db.Model):
    __tablename__       = "server_info"
    id                  = db.Column(db.Integer, db.ForeignKey("game_server.id"), primary_key = True)
    start_at            = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    stopped_at          = db.Column(db.DateTime, nullable=True)
    notes               = db.Column(db.Text, nullable=True)

    server = db.relationship("GameServer", back_populates="server_info")

    def __repr__(self):
        return f"<ServerInfo {self.id}>"
