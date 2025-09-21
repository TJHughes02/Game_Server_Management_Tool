from app import db
from datetime import datetime

#User table
class  User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_owner = db.Column(db.Boolean)
    display_name = db.Column(db.VARCHAR(80), nullable=False)
    pass_hash = db.Column(db.VARCHAR(120), nullable=False)

    def __repr__(self):
        return f"<User {self.id}>"

#Servers table
class Servers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.VARCHAR(80), nullable=False)
    game_type = db.Column(db.VARCHAR(80), nullable=False)
    #must add additional info i.e. status, ports, rcon info, etc

    def __repr__(self):
        return f"<Node {self.id}>"

#may change pending ERD and Relational Schema rework
class NodeUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Servers.id"), nullable=False)

    def __repr__(self):
        return f"<NodeUser {self.id}>"

#Server Info table
class ServerInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    server_id = db.Column(db.Integer, db.ForeignKey("Servers.id"), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now())
    #end_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<ServerInfo {self.id}>"
