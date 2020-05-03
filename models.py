
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

class Company(db.Model):
    """docstring for Company."""
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    logo = db.Column(db.LargeBinary)
    notes = db.Column(db.String(250), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    update_at = db.Column(db.DateTime, nullable=True)


    def __init__(self, name,email,phone,notes):
        self.name
        self.email
        self.phone
        self.notes
    def __repr__(self):
        return ("<Company| name : {}, email: {}".format(self.name,self.email))


major_levels = db.Table('levels',
    db.Column('level_id', db.Integer, db.ForeignKey('level.id'), primary_key=True),
    db.Column('major_id', db.Integer, db.ForeignKey('major.id'), primary_key=True)
)


class Majors(db.Model):

    __tablename__ = "major"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    levels = db.relationship('Levels', secondary=major_levels, lazy='subquery',backref=db.backref('level_id', lazy="dynamic"))
    notes = db.Column(db.String(250), nullable=True)
    create_at = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    update_at = db.Column(db.DateTime, nullable=True)

    student = db.relationship('Students', backref='majors', lazy=True)
    def __repr__(self):
        return ("<Majors| name : {}".format(self.name))


class Levels(db.Model):
    """docstring for Levels."""
    __tablename__ = 'level'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    notes = db.Column(db.String(250), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    update_at = db.Column(db.DateTime, nullable=True)
    student = db.relationship('Students', backref='level', lazy=True)

    def __repr__(self):
        return ("<Levels| name : {}".format(self.name))

class Subjects(db.Model):
    """docstring for Subjects."""
    __tablename__ = 'subjects'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    update_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return ("<Subjects| name : {}".format(self.name))



class Students(db.Model):
    """docstring for Students."""
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    un_id = db.Column(db.Integer, unique=True, nullable=False)
    create_at = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    update_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.String(250), nullable=True)

    major_id = db.Column(db.Integer, db.ForeignKey('major.id'),nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'),nullable=False)
    image = db.Column(db.LargeBinary, nullable = True)
    barcode_path = db.Column(db.String(200), nullable=True)


    def __repr__(self):
        return ("<Students| name : {}".format(self.name))
