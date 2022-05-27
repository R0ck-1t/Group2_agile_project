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
import random
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
  """User Table

  Args:
      db (Database): The application's database
      UserMixin (Class): Default methods for flask-login.
  """
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(24), unique=True)
  email = db.Column(db.String(50), unique=True)
  password = db.Column(db.String(80))
  bio = db.Column(db.String(512), default="")

class Replit(db.Model):
  """Replit Table

  Args:
      db (Database): The application's database
  """
  __tablename__ = 'replit'
  replit_id = db.Column(db.Integer, primary_key = True)
  replit_name = db.Column(db.String(128))
  replit_link = db.Column(db.String(256), unique=True)
  replit_uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  replit_description = db.Column(db.String(512), default = "")

class Comment(db.Model):
  """Comment Table

  Args:
      db (Database): The application's database
  """
  __tablename__ = 'comment'
  comment_id = db.Column(db.Integer, primary_key = True)
  replit_id = db.Column(db.Integer, db.ForeignKey('replit.replit_id'))
  content = db.Column(db.String(512))
  user = db.Column(db.String(24), db.ForeignKey('user.username'))

#These 2 lines create the database tables and commits the changes
db.create_all()
db.session.commit()


def ensure_test_account():
  # Checks that the default user is created and in the database, if not it will create the user.
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
  """Routing for direct url

  Returns:
      Redirect: Redirects to the user submissions page
  """
  return redirect(url_for('submissions'))

@app.route('/home', methods=['GET', 'POST'])
def index():
  """Routing for home button

  Returns:
      Redirect: Redirects to the featured replit page.
  """
  replits = Replit.query.all()
  id_num = random.choice(replits).replit_id
  form=commentForm()
  return redirect(url_for('view_content', form=form, replit_id_num=id_num))
  
@app.route('/view/<int:replit_id_num>', methods=['GET', 'POST'])
def view_content(replit_id_num):
  """Routing for user submission
  Users can view replit in embedded templit via iframe with a url that is fetched from the database based on the 'replit_id_num' in the url.
  Users can post comments if they are logged in via a comment form.
  
  Returns:
      Redirect: Redirects to the submission's page
  """
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
  """Routing for comment submission
  Empty function but ensures that there is a valid user logged in before accepting a submission
  """
  pass

@app.route('/delete_comment/<comment_id_num>', methods=['GET', 'DELETE'])
@login_required
def delete_comment(comment_id_num):
  """Deletes comment from the database

  Args:
      comment_id_num (int): The id number for the comment in the database

  Returns:
      Redirect: Redirects to the view_content routing and passes the same replit id to load the updated page.
  """
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
  """New Submission routing for the submission form

  Form with several fields that the user can fill out.
  When the user submits the form, the link is checked for validity and then the data is appended to the database.

  Returns:
      Redirect after submission: Returns you to the updated user submissions page
      Redirect on failed submission: Re-renders the new_submission template
  """
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
  #Gets all the replit submissions from the current logged in user.
  all_replits = Replit.query.all()
  uploader_replits = []
  for item in all_replits:
    if current_user.id == item.replit_uploader_id:
      uploader_replits.append(item)
  return uploader_replits

  
@app.route('/account-edit', methods=['GET', 'POST'])
@login_required
def account_edit():
  """Account Edit Routing

  User can fill out a form and then submit to replace their bio with the form's content.

  Returns:
      Redirect on Submit: Redirects to the account page without passing in the 'edit' bool
      Render: By default it renders the template of the account page with the edit interface visible by passing in a bool 'edit'.
  """
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
  """Account page routing 

  Returns:
      Render: Renders the templarte
  """
  form = UserForm()
  user_uploads = get_user_uploads()
  print(current_user)
  return render_template('account.html', name=current_user.username, email = current_user.email, bio=current_user.bio, form=form, uploads=user_uploads, edit=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
  """Login Routing

  Returns:
      Render: Renders the login form
      Return on submit: Redirect's you to your account page
  """
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
  """Signup routing page

  Renders a form the user can use to create an account
  Confirms all fields are filled properly
  On submission, runs the validate_on_submit() if statement.
  Returns:
      Render: Renders the sign-up form
      Return on submit: Redirect's you to your new account's page.
  """
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
  """Delete Replit routing

  Delete's the submission with the id number matching replit_id_num from the database and commits the change.

  Args:
      replit_id_num (int): Replit table row's id

  Returns:
      Redirect: Redirects to the user's account page.
  """
  replit = Replit.query.filter_by(replit_id = replit_id_num).first()
  Replit.query.filter_by(replit_id = replit_id_num).delete()
  db.session.commit()
  return redirect('/account')

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)

