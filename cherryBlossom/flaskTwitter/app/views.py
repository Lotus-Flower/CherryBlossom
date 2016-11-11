from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
	title = "Log In"
	return render_template('login.html')

@app.route('/newsfeed')
def newsfeed():
	title = "News Feed"
	return render_template('newsfeed.html')

@app.route('/test')
def test():
	title = "test"
	return render_template('testChild.html', title = title)

