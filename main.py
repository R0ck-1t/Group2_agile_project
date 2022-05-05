from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from src.loginform import LoginForm
from src.regform import RegisterForm
app = Flask('app')
app.config['SECRET_KEY'] = '2911DEMOKEYSUPERSECRET'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/home/runner/Demo2911Website/databases/data'
Bootstrap(app)
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(24), unique=True)
  email = db.Column(db.String(50), unique=True)
  password = db.Column(db.String(80))

@app.route('/', methods=['GET', 'POST'])
def home():
  return render_template('index.html')

  
@app.route('/')
def home1():
  return redirect('/login', code=200)


@app.route('/submissions')
def examples():
  return render_template('user_submissions.html')

@app.route('/account')
def documentation():
  return render_template('account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  return render_template('login.html', form=form)

@app.route('/signup')
def signup():
  form = RegisterForm()
  return render_template('signup.html', form=form)



@app.route('/projects/<variable>')
def to_do():
  pass

@app.route("/test")
def gitpage():
  return redirect('https://github.com/informationvulture/Group2_agile_project/')

app.run(host='0.0.0.0', port=8080)




