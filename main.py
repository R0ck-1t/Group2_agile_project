from flask import Flask, render_template, redirect, flash, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from src.loginform import LoginForm
from src.regform import RegisterForm
import os

app = Flask('app')
secret_key = "2911DEMOWEBSITESUPERSECRETKEY"

app.config['SECRET_KEY'] = "2911DEMOWEBSITESUPERSECRETKEY"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/database.db'

#changed above to only one folder

db = SQLAlchemy(app)
Bootstrap(app)


class User(db.Model):
  user_id = db.Column(db.Integer, primary_key = True)
  user_name = db.Column(db.String(24), unique=True)
  user_email = db.Column(db.String(50), unique=True)
  user_password = db.Column(db.String(80))
  user_bio = db.Column(db.String(500), default="")

class Replits(db.Model):
  replit_id = db.Column(db.Integer, primary_key = True)
  replit_name = db.Column(db.String(32))
  replit_description = db.Column(db.String(500), default = "")
    
db.create_all()
db.session.commit()

@app.route('/')
def home():
  return redirect('/submissions')



@app.route('/submissions')
def submissions():
  return render_template('user_submissions.html')

@app.route('/account')
def account():
  return render_template('account.html')

@app.route('/login', methods=['GET', 'POST'])

def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(user_name = form.user_name.data).first()
    if user:
      if (user.user_password == form.user_password.data):
        login(user, remember=form.remember.data)
        return redirect('/account')
    print("Submitted New User Account!")
    
  return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = RegisterForm()
  
  if form.validate_on_submit():
    check = User.query.filter_by(user_email = form.user_email.data).first()
    if form.user_password.data != form.user_confirm_password.data:
          flash("Passwords don't match.")
    elif form.user_email.data == check.user_email:
      flash("Email already in use.")
    else:
      new_user = User(user_name=form.user_name.data, user_email=form.user_email.data, user_password=form.user_password.data, user_bio = '')
      db.session.add(new_user)
      db.session.commit()
      print("Submitted New User Account!")
      return redirect('/login')
  return render_template('signup.html', form=form)



@app.route('/projects/<variable>')
def to_do():
  pass

@app.route("/test")
def gitpage():
  return redirect('https://github.com/informationvulture/Group2_agile_project/')

app.run(host='0.0.0.0', port=8080)

