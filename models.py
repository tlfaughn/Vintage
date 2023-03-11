from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    first = db.Column(db.String(150), nullable=True, default='')
    last = db.Column(db.String(150), nullable=True, default='')
    username = db.Column(db.String(150), nullable=True, default='')
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    cars = db.relationship('Car', backref='user', lazy=True)

    def __init__(self, first='', last='', username='', email='', password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.first = first
        self.last = last
        self.username = username
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} also know as {self.username} has been added to the database'

class Car(db.Model):
    Vin = db.Column(db.String(17), primary_key=True)
    Make = db.Column(db.String(150), nullable=False)
    Model = db.Column(db.String(150), nullable=False)
    Year = db.Column(db.String(4))
    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False, default='')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.Year} {self.Make} {self.Model} by {self.user_id} has been added to the database'
    

    def __init__(self, Vin, Make, Model, Year, user_id):
        self.Vin = Vin
        self.Make = Make
        self.Model = Model
        self.Year = Year
        self.user_id = user_id

class CarSchema(ma.Schema):
    class Meta:
        fields = ['Vin','Make', 'Model', 'Year','user_id']

car_schema = CarSchema()
cars_schema = CarSchema(many=True)