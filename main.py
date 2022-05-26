from unicodedata import name
from flask import Flask, render_template, redirect, flash, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import all_
from src.loginform import LoginForm
from src.regform import RegisterForm
from src.userform import UserForm
from src.commentform import commentForm
from src.submissionform import submissionForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import sqlite3, json
app = Flask('app')
with open("./private/key.txt") as key_file:
  app.config['SECRET_KEY'] = key_file.read()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/database.db'

# changed above to only one folder

db = SQLAlchemy(app)
Bootstrap(app) 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
  return User.query.get(int(id))

class User(db.Model, UserMixin):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(24), unique=True)
  email = db.Column(db.String(50), unique=True)
  password = db.Column(db.String(80))
  bio = db.Column(db.String(512), default="")

class Replit(db.Model):
  __tablename__ = 'replit'
  replit_id = db.Column(db.Integer, primary_key = True)
  replit_name = db.Column(db.String(128))
  replit_link = db.Column(db.String(256), unique=True)
  replit_uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  replit_description = db.Column(db.String(512), default = "")

class Comment(db.Model):
  __tablename__ = 'comment'
  comment_id = db.Column(db.Integer, primary_key = True)
  replit_id = db.Column(db.Integer, db.ForeignKey('replit.replit_id'))
  content = db.Column(db.String(512))
  user = db.Column(db.String(24), db.ForeignKey('user.username'))

db.create_all()
db.session.commit()
def ensure_test_account():
  test_user = User.query.filter_by(username = 'TestUsername').first()
  if test_user:
    pass
  else:
    new_user = User(username="TestUsername", email="TestEmailAgile@scrum.ca", password=generate_password_hash("password", method='sha256'), bio='test bio')
    db.session.add(new_user)
    db.session.commit()
ensure_test_account()


@app.route('/')
def home():
  return redirect(url_for('submissions'))

@app.route('/home', methods=['GET', 'POST'])
def index():
  form=commentForm()
  return redirect(url_for('view_content', form=form, replit_id_num=3))
  
@app.route('/view/<int:replit_id_num>', methods=['GET', 'POST'])
def view_content(replit_id_num):
  form = commentForm()
  replit_submission = Replit.query.filter_by(replit_id = replit_id_num).first()
  all_comments = Comment.query.all()
  post_comments = []
  for row in all_comments:
    print(f"Comment: {row.content}\nReplit ID: {row.replit_id} - Current Replit ID: {replit_id_num}")
    if row.replit_id == replit_id_num:
      post_comments.append(row)
  if form.validate_on_submit():
    new_comment = Comment(content=form.content.data, user=current_user.username, replit_id = replit_id_num)
    for item in post_comments:
      if item.content == new_comment.content:
        if item.user == current_user.username:
          return redirect(url_for('view_content', replit_id_num=replit_id_num))
    db.session.add(new_comment)
    print(new_comment)
    db.session.commit()
    form.content.data = ""
  all_comments = Comment.query.all()
  post_comments = []
  for row in all_comments:
    print(f"Comment: {row.content}\nReplit ID: {row.replit_id} - Current Replit ID: {replit_id_num}")
    if row.replit_id == replit_id_num:
      post_comments.append(row)
  return render_template('replit_page.html', form=form, comments = post_comments, replit_name=replit_submission.replit_name, description=replit_submission.replit_description, link = replit_submission.replit_link)


@app.route('/submit_comment')
@login_required
def submit_comment():
  pass

@app.route('/delete_comment/<comment_id_num>', methods=['GET', 'DELETE'])
@login_required
def delete_comment(comment_id_num):
  comment = Comment.query.filter_by(comment_id = comment_id_num).first()
  replit_id = comment.replit_id
  Comment.query.filter_by(comment_id = comment_id_num).delete()
  db.session.commit()
  return redirect(url_for('view_content', replit_id_num = replit_id))

@app.route('/submissions', methods=['GET'])
def submissions():
  replits = Replit.query.all()
  if current_user.is_authenticated:
    return render_template('user_submissions.html', name=current_user.username, email = current_user.email, bio=current_user.bio, replits=replits)
  else:
    return render_template('user_submissions.html', replits=replits)

@app.route('/new_submission', methods=['GET', 'POST'])
@login_required
def new_submission():
  form = submissionForm()
  if form.validate_on_submit():
    if 'replit.com' not in form.replit_link.data.lower():
      flash('Error. Invalid URL.', 'error')
      return
    else:
      url = form.replit_link.data.split('#')
      url = url[0]
      url = url.split('?')
      url = url[0] + '?embed=true'
    new_replit = Replit(replit_link=url, replit_name=form.replit_name.data, replit_description=form.replit_description.data, replit_uploader_id=current_user.id)
    db.session.add(new_replit)
    db.session.commit()
    return redirect(url_for('submissions'))
  return render_template('new_submission.html', form=form, edit=False, name=current_user.username)

def get_user_uploads():
  all_replits = Replit.query.all()
  uploader_replits = []
  for item in all_replits:
    if current_user.id == item.replit_uploader_id:
      uploader_replits.append(item)
  return uploader_replits

  
@app.route('/account-edit', methods=['GET', 'POST'])
@login_required
def account_edit():
  form = UserForm()
  print(current_user)
  user_uploads = get_user_uploads()
  if form.validate_on_submit():
    current_user.bio = form.bio.data
    db.session.commit()
    return redirect(url_for('account'))
  return render_template('account.html', name=current_user.username, email = current_user.email, bio=current_user.bio, form=form, uploads=user_uploads, edit=True)

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  form = UserForm()
  user_uploads = get_user_uploads()
  print(current_user)
  return render_template('account.html', name=current_user.username, email = current_user.email, bio=current_user.bio, form=form, uploads=user_uploads, edit=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username = form.username.data).first()
    if user:
      if check_password_hash(user.password, form.password.data):
        login_user(user, remember=form.remember.data)
        return redirect(url_for('account'))
    
  return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = RegisterForm()
  
  if form.validate_on_submit():
    check = User.query.filter_by(email = form.email.data).first()
    if form.password.data != form.user_confirm_password.data:
      print("Passwords don't match.")
    elif check:
      print("Email already in use.")
    else:
      hashed_password = generate_password_hash(form.password.data, method='sha256')
      new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, bio='')
      db.session.add(new_user)
      db.session.commit()
      print("Submitted New User Account!")
      return redirect('/login')
  return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect('/login')


@app.route('/delete_replit/<replit_id_num>', methods=['GET', 'DELETE'])
@login_required
def delete_replit(replit_id_num):
  replit = Replit.query.filter_by(replit_id = replit_id_num).first()
  Replit.query.filter_by(replit_id = replit_id_num).delete()
  db.session.commit()
  return redirect('/account')

@app.route("/test")
def gitpage():
  return redirect('https://github.com/informationvulture/Group2_agile_project/')



if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)

