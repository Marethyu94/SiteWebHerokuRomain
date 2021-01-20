from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True) # primary keys are required by SQLAlchemy
    identifiant = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    numsecu = db.Column(db.Integer())
    last_name = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    age = db.Column(db.Integer())
    adresse1 = db.Column(db.String(1000))
    adresse2 = db.Column(db.String(1000))
    taille = db.Column(db.Integer())
    poids = db.Column(db.Integer())
    allergie = db.Column(db.String(10))
    malchr = db.Column(db.String(10))
    picidentity = db.Column(db.LargeBinary())

class Resultat(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    numsecu = db.Column(db.Integer())
    result_analyse = db.Column(db.String())