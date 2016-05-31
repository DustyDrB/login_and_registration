from flask import Flask, flash, render_template, request, redirect, session
from mysqlconnection import MySQLConnector
import re
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
mysql = MySQLConnector(app, 'email')
app.secret_key = "adorable_beagles"

mail_val = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():

	return redirect('/')

@app.route('/register', methods=['POST'])
def add_user():
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

  		query = "INSERT INTO users (first_name, last_name, email, password, updated_at, created_at) VALUES (:first_name, :last_name, :email, :pass, NOW(), NOW()")
		pw_hash = bcrypt.generate_password_hash(reqest.form['password'])
		data = {
			first_name: request.form['first_name']
			last_name: request.form['last_name']
			email: request.form['email']
			password: request.form['password'] 
		}
		mysql.query_db(query, data)
		return redirect('/')

	return redirect('/')

if __name__ =="__main__":
	app.run(debug=True)