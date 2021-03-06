from flask import render_template, redirect, flash, url_for, request
from app import app, db
from app.forms import LoginForm, RegisterForm, EditProfileForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse
from datetime import datetime

@app.before_request
def before_request():
  if current_user.is_authenticated:
    current_user.last_seen = datetime.utcnow()
    db.session.commit()

@app.route('/')
def index():
  return render_template('index.html', title='Home', posts=Post.query.all())

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)
  return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegisterForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash(f"Congratulations, {user.username}, you are now registered!")
    login_user(user)
    return redirect(url_for('index'))
  return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/secure')
@login_required
def secure():
  return render_template('secure.html')

@app.route('/user/<username>')
@login_required
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  posts = user.posts.all()
  return render_template('user.html', user=user, posts=posts)

@app.route('/user/<username>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EditProfileForm(current_user)
    if form.validate_on_submit():
      current_user.username = form.username.data
      current_user.about_me = form.about_me.data
      db.session.commit()
      flash('Your changes have been saved.')
      return redirect(url_for('edit_user', username=current_user.username))
    elif request.method == 'GET' and current_user.username is user.username:
      form.username.data = current_user.username
      form.about_me.data = current_user.about_me
      return render_template('edit_profile.html', title='Edit Profile', form=form, cancel=request.referrer)

# API ROUTE TO PLAY WITH MITHRIL
@app.route('/api/user/<username>')
@login_required
def info(username):
    user = User.query.filter_by(username=username).first_or_404()
    if (current_user.username is user.username):
      return { "about_me": current_user.about_me, "username": current_user.username }