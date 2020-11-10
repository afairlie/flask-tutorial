from flask import render_template, redirect, flash
from app import app
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user
from app.models import User

@app.route('/')
def index():
  user = {'username': 'Ariane'}
  posts = [
    {
        'author': {'username': 'John'},
        'body': 'Beautiful day in Portland!'
    },
    {
        'author': {'username': 'Susan'},
        'body': 'The Avengers movie was so cool!'
    }
  ]
  return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect('/')
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect('/login')
    login_user(user, remember=form.remember_me.data)
    return redirect('/')
  return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegisterForm()
  if form.validate_on_submit():
    flash(f"{form.username.data} registered with email: {form.email.data}")
    return redirect('/')
  return render_template('login.html', title='Register', form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect('/')

@app.route('/hello')
def hello():
  return render_template('hello from the app')