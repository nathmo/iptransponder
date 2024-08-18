from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class PacketLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer, nullable=False)
    src_ip = db.Column(db.String(45), nullable=False)
    dest_ip = db.Column(db.String(45), nullable=False)
    src_port = db.Column(db.Integer, nullable=False)
    dest_port = db.Column(db.Integer, nullable=False)
    protocol = db.Column(db.String(10), nullable=False)
    ping_back = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return f'<PacketLog {self.src_ip} -> {self.dest_ip}>'
