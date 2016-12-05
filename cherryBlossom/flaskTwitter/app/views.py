from app import app, db
from flask import render_template, flash, redirect, url_for, g, request
from flask_login import login_required, login_user, logout_user, current_user
import json
import datetime
from .forms import LoginForm, RegisterForm, TweetForm, CommentForm, SearchForm
from .models import User, Tweet, Comment

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

@app.route('/register', methods=['GET', 'POST'])
def register():
	title = "Register"
	form = RegisterForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, password=form.password_hash.data, fName=form.fName.data, lName=form.lName.data, email=form.email.data)
		db.session.add(user)
		db.session.commit()
		db.session.add(user.follow(user))
		db.session.commit()
		login_user(user)
		return redirect(url_for('newsfeed'))
	return render_template('register.html', title = title, form = form)

@app.route('/newsfeed', methods=['GET', 'POST'])
@login_required
def newsfeed():
	title = "News Feed"
	user = g.user
	form = TweetForm()
	commentForm = CommentForm()
	searchForm = SearchForm()
	tweets = user.followed_tweets().all()
	numTweets = user.tweets.count()
	followed = user.followed.count()

	firstTweet = tweets[0]
	lastTweet = tweets[-1]

	if searchForm.validate_on_submit():
		searchUser = searchForm.username.data
		if searchUser is None:
			return redirect(url_for('newsfeed'))
		else:
			validUser = False
			for u in User.query.all():
				if searchUser == u.username:
					validUser = True
			if validUser:
				return redirect(url_for('profile', username=searchUser))
			else:
				return redirect(url_for('error', errorType="search"))


	return render_template('newsfeed.html', title = title, user = user, form = form, commentForm=commentForm, searchForm=searchForm, tweets = tweets, firstTweet=firstTweet, lastTweet=lastTweet, numTweets=numTweets, followed=followed)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/storeTweet', methods=['POST'])
@login_required
def storeTweet():
	user = g.user
	form = TweetForm()

	tweet = Tweet(body=form.body.data, timestamp=datetime.datetime.now(), hearts=0, user_id=user.id)
	db.session.add(tweet)
	db.session.commit()

	# tweetBody = request.form['body'];
	currentTweet = Tweet.query.filter_by(timestamp=tweet.timestamp).first()
	tweetID = currentTweet.id
    
	return json.dumps({'body': form.body.data, 'tweetID': tweetID})

@app.route('/storeComment', methods=['POST'])
@login_required
def storeComment():
	user = g.user
	form = CommentForm()

	index = request.json['index']
	body = request.json['body']

	comment = Comment(body=body, timestamp=datetime.datetime.now(), tweet_id=index, user_id=user.id)
	db.session.add(comment)
	db.session.commit()

	currentComment = Comment.query.filter_by(timestamp=comment.timestamp).first()
	commentID = currentComment.id
    
	# return form.body.data

	return json.dumps({'index': index, 'commentID': commentID, 'gravatar': user.avatar_hash, 'username': user.username, 'fName': user.fName, 'lName': user.lName})
	

@app.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		return redirect(url_for('index'))
	u = g.user.follow(user)
	if u is None:
		return redirect(url_for('profile', username=username))
	db.session.add(u)
	db.session.commit()
	return redirect(url_for('profile', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		return redirect(url_for('index'))
	u = g.user.unfollow(user)
	if u is None:
		return redirect(url_for('profile', username=username))
	db.session.add(u)
	db.session.commit()
	return redirect(url_for('profile', username=username))

@app.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):

	validUser = False

	for u in User.query.all():
		if u.username == username:
			validUser = True

	if not validUser:
		return redirect(url_for('error', errorType="search"))

	title = username
	user = User.query.filter_by(username=username).first()
	form = CommentForm()
	searchForm = SearchForm()
	currUser = g.user
	tweets = user.tweets.order_by(Tweet.timestamp.desc())
	firstTweet = tweets[0]
	lastTweet = tweets[-1]

	numTweets = user.tweets.count()
	followed = user.followed.count()

	if searchForm.validate_on_submit():
		searchUser = searchForm.username.data
		if searchUser is None:
			return redirect(url_for('newsfeed'))
		else:
			validUser = False
			for u in User.query.all():
				if searchUser == u.username:
					validUser = True
			if validUser:
				return redirect(url_for('profile', username=searchUser))
			else:
				return redirect(url_for('error', errorType="search"))

	if(user in currUser.followed):
		canFollow = False
	else:
		canFollow = True

	if user == None:
		return redirect(url_for('newsfeed'))
	return render_template('profile.html', title=title, user=user, currUser=currUser, form=form, searchForm=searchForm, canFollow=canFollow, tweets=tweets, firstTweet=firstTweet, lastTweet=lastTweet, numTweets=numTweets, followed=followed)

@app.route('/searchResults', methods=['GET'])
@login_required
def searchResults():
	resultsJSON = []
	users = User.query.all()

	for user in users:
		username = user.username
		resultsJSON.append(username)

	return json.dumps(resultsJSON)

@app.route('/error/<errorType>')
def error(errorType):
	title = "Error"

	if errorType == "search":
		errorDesc = "Search Error"
		body = "The specified user could not be found."
	elif errorType == "404":
		errorDesc = "404"
		body = "The specified page could not be found."
	else:
		errorDesc = "FlaskTwitter"
		body = "The specified page could not be found."

	return render_template('error.html', title=title, errorDesc=errorDesc, body=body)

@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('error', errorType="404"))