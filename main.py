from flask import Flask, render_template, redirect, flash, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from src.loginform import LoginForm
from src.regform import RegisterForm
import os

app = Flask('app')
secret_key = os.environ['SECRET_KEY_VAR']

app.config['SECRET_KEY'] = secret_key

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/runner/Demo2911Website/databases/database.db'

#changed above to only one folder

db = SQLAlchemy(app)
Bootstrap(app)


class User(db.Model):
  user_id = db.Column(db.Integer, primary_key = True)
  user_name = db.Column(db.String(24), unique=True)
  user_email = db.Column(db.String(50), unique=True)
  user_password = db.Column(db.String(80))
  user_bio = db.Column(db.String(500), default="")
    
db.create_all()
db.session.commit()

@app.route('/')
def home():
  return render_template('replit_page.html')

  
@app.route('/')
def home1():
  return render_template('user_submissions.html')


@app.route('/submissions')
def examples():
  return render_template('user_submissions.html')

@app.route('/account')
def documentation():
  return render_template('account.html')

@app.route('/login', methods=['GET', 'POST'])

def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username = form.username.data).first()
    if user:
      if (user.password == form.password.data):
        login(user, remember=form.remember.data)
        return redirect(url_for('account'))
    print("Submitted New User Account!")
    
  return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = RegisterForm()
  
  if form.validate_on_submit():
    if form.password.data != form.confirm_password.data:
      flash("Passwords don't match.")
    else:
      new_user = User(user_name=form.username.data, user_email=form.email.data, user_password=form.password.data,user_bio = '')
      db.session.add(new_user)
      db.session.commit()
      print("Submitted New User Account!")
      return redirect(url_for('login'))
  return render_template('signup.html', form=form)



@app.route('/projects/<variable>')
def to_do():
  pass

@app.route("/test")
def gitpage():
  return redirect('https://github.com/informationvulture/Group2_agile_project/')

app.run(host='0.0.0.0', port=8080)

