from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# LOOK INTO RELATIONSHIPS FOR STREAMLINING QUERIES

#User table
class  User(db.Model):
    __tablename__   = 'user'
    id              = db.Column(db.Integer, primary_key=True)
    email           = db.Column(db.String(255), unique=True)
    is_owner        = db.Column(db.Boolean)
    display_name    = db.Column(db.VARCHAR(80), unique=True, nullable=False)
    pass_hash       = db.Column(db.VARCHAR(120), nullable=False)

    def __repr__(self):
        return f"<User {self.id}>"

    def set_pass(self, password):
        self.pass_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pass_hash, password)

#Game Server User table
class GameServerUser(db.Model):
    __tablename__   = 'game_server_user'
    user_id         = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    server_id       = db.Column(db.Integer, db.ForeignKey('game_server.id'), primary_key=True)
    role            = db.Column(db.VARCHAR(50), nullable=False)



#Servers table
class GameServer(db.Model):
    __tablename__   = 'game_server'
    id              = db.Column(db.Integer, primary_key=True)
    name            = db.Column(db.VARCHAR(120), nullable=False)
    game_type       = db.Column(db.VARCHAR(120), nullable=False)
    status          = db.Column(db.Enum("running", "stopped", "updating", name="server_status"), nullable=False)
    server_port     = db.Column(db.Integer, nullable=False)
    install_path    = db.Column(db.VARCHAR(255), nullable=False)
    archive_path    = db.Column(db.VARCHAR(255), nullable=True)
    backup_path     = db.Column(db.VARCHAR(255), nullable=True)


    def __repr__(self):
        return f"<Node {self.id}>"

class RconConfig(db.Model):
    __tablename__ = 'rcon_config'
    id = db.Column(db.Integer, db.ForeignKey('game_server.id'), primary_key=True)
    server_host_name = db.Column(db.VARCHAR(120), nullable=False)
    rcon_port = db.Column(db.VARCHAR(255), nullable=False)

#Server Info table
class ServerInfo(db.Model):
    __tablename__ = 'server_info'
    id = db.Column(db.Integer, db.ForeignKey("servers.id"), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now())
    #end_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<ServerInfo {self.id}>"



'''
#may change pending ERD and Relational Schema rework
class NodeUser(db.Model):
    __tablename__ = 'node_user'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("servers.id"), nullable=False)

    def __repr__(self):
        return f"<NodeUser {self.id}>"
'''