from flask import Flask, flash, render_template, request, redirect, session
from mysqlconnection import MySQLConnector
import re
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
mysql = MySQLConnector(app, 'loginreg')
app.secret_key = "adorable_beagles"

mail_val = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
num_check = re.compile('[0-9]')
case_check = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])')

@app.route('/', methods=['GET'])
def index():
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
	email = request.form['email']
	password = request.form['password']
	query = "SELECT * FROM users WHERE email= :email LIMIT 1"
	data = {
		'email': request.form['logemail'],
		'password': request.form['logpass']
	}
	mysql.query_db(query, data)
	user = mysql.query_db(query, data)
	email = mysql.query_db(query, data)[0]
	if bcrypt.check_password_hash(user[0]['pw_hash'], password):
		return render_template('/', email=email)
	else:
		flash('Incorrect password')
		return redirect('/')

@app.route('/register', methods=['POST', 'GET'])
def add_user():
	session['first_name'] = request.form['first_name']
	session['last_name'] = request.form['last_name']
	session['email'] = request.form['email']
	session['pass'] = request.form['pass']
	session['confirm_pass'] = request.form['confirm_pass']

	if len(request.form['first_name']) < 1:
		flash('First Name cannot be empty!')
		return redirect('/')
	elif num_check.search(request.form['first_name']) != None:
		flash("First name can't have numbers")
		return redirect('/')
	elif len(request.form['last_name']) < 1:
		flash('Last Name cannot be empty!')
		return redirect('/')
	elif num_check.search(request.form['last_name']) != None:
		flash("Last name can't have numbers")
		return redirect('/')
	elif len(request.form['email']) < 1:
		flash['Email cannot be empty!']
	elif not mail_val.match(request.form['email']):
		flash('Your email is not valid!')
		return redirect('/')
	elif len(request.form['password']) < 8:
		flash("Password cannot contain less than eight characters")
		return redirect('/')
	elif not case_check.match(request.form['password']):
		flash("Password must contain at least one upper case and one lower case letter!")
		return redirect('/')
	elif len(request.form['confirm_pass']) < 8:
		flash("Password cannot contain less than eight characters")
		return redirect('/')
	elif request.form['password'] != request.form['confirm_pass']:
		flash("Your passwords do not match!")
		return redirect('/')
  	else:
  		flash("Registration successful! Thank you!")
  		first_name = request.form['first_name']
		last_name = request.form['last_name']
		email = request.form['email']
		password = request.form['password']
  		user_query = "INSERT INTO users (first_name, last_name, email, password, updated_at, created_at) VALUES (:first_name, :last_name, :email, :pass, NOW(), NOW())"
		data = {
			'first_name': request.form['first_name'],
			'last_name': request.form['last_name'],
			'email': request.form['email'],
			'pw': request.form['password'],
		}
		pw_hash = bcrypt.generate_password_hash(password)
		mysql.query_db(user_query, data)
		return redirect('/')

	return redirect('/')

if __name__ =="__main__":
	app.run(debug=True)