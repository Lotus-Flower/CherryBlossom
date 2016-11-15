from app import app, db
from flask import render_template, flash, redirect, url_for, g
from flask_login import login_required, login_user, logout_user, current_user
from .forms import LoginForm, RegisterForm
from .models import User

@app.before_request
def before_request():
    g.user = current_user

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	title = "Log In"
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first_or_404()
		if user.is_correct_password(form.password_hash.data):
			login_user(user)
			return redirect(url_for('newsfeed'))
		else:
			return redirect(url_for('index'))
	return render_template('login.html', title = title, form = form)

@app.route('/newsfeed')
@login_required
def newsfeed():
	title = "News Feed"
	user = g.user
	return render_template('newsfeed.html', title = title, user = user)

@app.route('/register', methods=['GET', 'POST'])
def register():
	title = "Register"
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, password=form.password_hash.data, fName=form.fName.data, lName=form.lName.data, email=form.email.data)
		db.session.add(user)
		db.session.commit()
		login_user(user)
		return redirect(url_for('newsfeed'))
	return render_template('register.html', title = title, form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



@app.route('/test', methods=['GET', 'POST'])
def test():
	title = "test"
	form = RegisterForm()
	if form.validate_on_submit():
		flash('Login requested for ' + form.username.data + ', with password ' + form.password.data + ' and ' + str(form.rememberMe.data))
	return render_template('testChild.html', title = title, form = form)

