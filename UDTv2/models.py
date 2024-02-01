from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from UDTv2 import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(UserMixin, db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.String(1024), nullable=False)

    @property
    def password(self):
        raise AttributeError('Password is not readable')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    

    def __repr__(self):
        return f"User: {self.name}"
    
class Sites(db.Model):
    siteID = db.Column(db.String(6), nullable=False, unique=True, primary_key=True)
    siteName = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip = db.Column(db.String(100))
    owner = db.Column(db.String(50))
    parish = db.Column(db.String(50))
    coordinates = db.Column(db.String(50))
    manufacturer = db.Column(db.String(50))
    model = db.Column(db.String(50))
    serial = db.Column(db.String(50))
    refrigerant = db.Column(db.String(50))
    controller = db.Column(db.String(50))
    type_of = db.Column(db.String(25))
    filters = db.Column(db.String(50))
    
    def __repr__(self):
        return f"Site: {self.siteID} {self.siteName}"