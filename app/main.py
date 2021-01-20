from flask import render_template, request, Blueprint, redirect, url_for, make_response, json
from . import db
from flask_login import login_required, current_user
from .models import User, Resultat
import base64
import os

main = Blueprint('main', __name__)

def writeTofile(data):
	with open(data, 'w') as file:
		pdf = file.write(data)
		file.close()
		return pdf


@main.route('/accueil')
@login_required
def accueil():
	file_data = User.query.filter_by(identifiant=current_user.identifiant).first()
	image = base64.b64encode(file_data.picidentity).decode('ascii')
	return render_template("accueil.html", image=image)



@main.route('/info-perso')
@login_required
def infoperso():
	file_data = User.query.filter_by(identifiant=current_user.identifiant).first()
	image = base64.b64encode(file_data.picidentity).decode('ascii')
	myinfo = {
	'last_name': User.query.filter_by(identifiant=current_user.identifiant).first().last_name,
	'first_name': User.query.filter_by(identifiant=current_user.identifiant).first().first_name,
	'age': User.query.filter_by(identifiant=current_user.identifiant).first().age,
	'adresse1': User.query.filter_by(identifiant=current_user.identifiant).first().adresse1,
	'adresse2': User.query.filter_by(identifiant=current_user.identifiant).first().adresse2,
	'taille': User.query.filter_by(identifiant=current_user.identifiant).first().taille,
	'poids': User.query.filter_by(identifiant=current_user.identifiant).first().poids,
	'allergie': User.query.filter_by(identifiant=current_user.identifiant).first().allergie,
	'malchr': User.query.filter_by(identifiant=current_user.identifiant).first().malchr,
	}
	return render_template('info_perso.html', myinfo=myinfo, image=image)


@main.route('/maj-info')
@login_required
def changeinfo():
	file_data = User.query.filter_by(identifiant=current_user.identifiant).first()
	image = base64.b64encode(file_data.picidentity).decode('ascii')
	return render_template("info_perso_modif.html", image=image)

@main.route('/maj-info', methods=['POST'])
@login_required
def changeinfo_post():
	updateinfo = {}

	file = request.files['picidentity']
	print(file)
	updateinfo['last_name'] = request.form.get('lastname')
	updateinfo['first_name'] = request.form.get('firstname')
	updateinfo['age'] = request.form.get('age')
	updateinfo['adresse1'] = request.form.get('adresse1')
	updateinfo['adresse2'] = request.form.get('adresse2')
	updateinfo['taille'] = request.form.get('taille')
	updateinfo['poids'] = request.form.get('poids')
	updateinfo['allergie'] = request.form.get('allergie')
	updateinfo['malchr'] = request.form.get('malchr')
	print(request.form.get('age'))
	print(request.form.get('taille'))

	user = User.query.filter_by(identifiant=current_user.identifiant).first()

	if updateinfo['last_name'] == '':
		pass
	else:
		user.last_name = updateinfo['last_name']

	if updateinfo['first_name'] == '':
		pass
	else:
		user.first_name = updateinfo['first_name'] 

	if updateinfo['age'] == 'Choose...':
		pass
	else:
		updateinfo['age'] = int(updateinfo['age'])
		user.age = updateinfo['age'] 

	if updateinfo['adresse1'] == '':
		pass
	else:
		user.adresse1 = updateinfo['adresse1'] 

	if updateinfo['adresse2'] == '':
		pass
	else:
		user.adresse2 = updateinfo['adresse2']

	if updateinfo['taille'] == 'Choose...':
		pass
	else: 
		updateinfo['taille'] = int(updateinfo['taille'])
		user.taille = updateinfo['taille']

	if updateinfo['poids'] == 'Choose...':
		pass
	else:
		updateinfo['poids'] = int(updateinfo['poids'])
		user.poids = updateinfo['poids']

	if updateinfo['allergie'] == 'Choose...':
		pass
	else:
		user.allergie = updateinfo['allergie']

	if updateinfo['malchr'] == 'Choose...':
		pass
	else:
		user.malchr = updateinfo['malchr'] 

	if file.filename:
		data = file.read()
		user.picidentity = data
	else:
		pass
	db.session.commit()



	return redirect(url_for('main.infoperso'))


@main.route('/last-results')
@login_required
def lastresult():
	list_pdf = []
	file_data = User.query.filter_by(identifiant=current_user.identifiant).first()
	image = base64.b64encode(file_data.picidentity).decode('ascii')
	pdf_data = Resultat.query.filter_by(numsecu=current_user.numsecu).all()
	for i in pdf_data:
		path_pdf = i.result_analyse
		list_pdf.append(path_pdf)
	
	return render_template("lastresult.html", image=image, pdf=list_pdf)

@main.route('/all-results')
@login_required
def allresult():
	list_pdf2 = []
	file_data = User.query.filter_by(identifiant=current_user.identifiant).first()
	image = base64.b64encode(file_data.picidentity).decode('ascii')
	pdf_data = Resultat.query.filter_by(numsecu=current_user.numsecu).all()
	for i in pdf_data:
		path_pdf = i.result_analyse
		list_pdf2.append(path_pdf)
	nbfile = len(list_pdf2)
	return render_template("allresults.html", image=image, pdf=json.dumps(list_pdf2), nbfile=nbfile)
