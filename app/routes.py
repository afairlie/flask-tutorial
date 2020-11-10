from flask import render_template, redirect, flash
from app import app
from app.forms import LoginForm, RegisterForm

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
  form = LoginForm()
  if form.validate_on_submit():
    flash(f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}")
    return redirect('/')
  return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegisterForm()
  if form.validate_on_submit():
    flash(f"{form.username.data} registered with email: {form.email.data}")
    return redirect('/')
  return render_template('login.html', title='Register', form=form)

@app.route('/hello')
def hello():
  return render_template('hello from the app')