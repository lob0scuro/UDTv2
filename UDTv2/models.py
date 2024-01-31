from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from UDTv2 import db


class Users(UserMixin, db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"User: {self.name}"
    
