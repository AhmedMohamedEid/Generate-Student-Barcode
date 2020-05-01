
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()



class Users(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250),nullable=False)
    create_at = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    update_at = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime,index=False,unique=False,nullable=True)

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __init__(self, name,username,email,password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return ("<User {}- email {}.>".format(self.name,self.email))

class Company(models.Model):
    """docstring for Company."""
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    def __init__(self, arg):
        super(Company, self).__init__()
        self.arg = arg
