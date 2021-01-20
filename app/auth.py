from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Resultat
from . import db
from flask_login import login_user, logout_user, login_required
import os


auth = Blueprint('auth', __name__)

def convertToBinaryData():
    #Convert digital data to binary format
    with open('app\\static\\pic_identite_anonyme.png', 'rb') as file:
        blobData = file.read()
    return blobData

@auth.route('/')
def login():
    return render_template("login.html")

@auth.route('/', methods=['POST'])
def login_post():
	identifiant = request.form.get('identifiant')
	password = request.form.get('password')
	remember = True if request.form.get('remember') else False

	user = User.query.filter_by(identifiant=identifiant).first()

	if not user or not check_password_hash(user.password, password):
		flash('Please check your login details and try again.')
		return redirect(url_for('auth.login'))

	login_user(user, remember=remember)
	return redirect(url_for('main.accueil'))

@auth.route('/signup')
def signup():
	return render_template("signup.html")

@auth.route('/signup', methods=['POST'])
def signup_post():
	identifiant = request.form.get('identifiant')
	numsecu = request.form.get('numsecu')
	password = request.form.get('password')
	image = convertToBinaryData()

	user = User.query.filter_by(identifiant=identifiant).first() #if this returns a user, then the email already exists in database

	if user:
		flash('Email address already exists !')
		return redirect(url_for('auth.signup'))

	new_user = User(identifiant=identifiant, numsecu=numsecu, password=generate_password_hash(password, method='sha256'), picidentity=image)

	db.session.add(new_user)
	db.session.commit()

	return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('auth.login'))