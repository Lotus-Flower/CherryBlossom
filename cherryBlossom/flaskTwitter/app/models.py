from app import db, bcrypt
from flask import request
from sqlalchemy.ext.hybrid import hybrid_property
import hashlib

followers = db.Table('followers',
	db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
	db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(16), index=True, unique=True)
	password_hash = db.Column(db.String(128), index=True)
	fName = db.Column(db.String(30), index=True)
	lName = db.Column(db.String(30), index=True)
	email = db.Column(db.String(120), index=True, unique=True)
	avatar_hash = db.Column(db.String(32), index=True)
	tweets = db.relationship('Tweet', backref='author', lazy='dynamic')
	comments = db.relationship('Comment', backref='author', lazy='dynamic')
	followed = db.relationship('User', secondary=followers, primaryjoin=(followers.c.follower_id == id), secondaryjoin=(followers.c.followed_id == id), backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
	
	@hybrid_property
	def password(self):
		return self.password_hash

	def is_correct_password(self, plaintext):
		return bcrypt.check_password_hash(self.password_hash, plaintext)

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)

	def gravatar(self, size=100, default='identicon', rating='g'):
		if request.is_secure:
			url = 'https://secure.gravatar.com/avatar'
		else:
			url = 'http://www.gravatar.com/avatar'
		hash = self.avatar_hash or hashlib.md5(self.email.encode('utf-8')).hexdigest()
		return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(url=url, hash=hash, size=size, default=default, rating=rating)

	def follow(self, user):
		if not self.is_following(user):
			self.followed.append(user)
			return self

	def unfollow(self, user):
		if self.is_following(user):
			self.followed.remove(user)
			return self

	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

	def followed_tweets(self):
		return Tweet.query.join(followers, (followers.c.followed_id == Tweet.user_id)).filter(followers.c.follower_id == self.id).order_by(Tweet.timestamp.desc())

	def __init__(self, username, password_hash, fName, lName, email):
		self.username = username
		self.password_hash = bcrypt.generate_password_hash(password_hash)
		self.fName = fName
		self.lName = lName
		self.email = email
		self.tweets = []
		self.followed = []
		if self.email is not None and self.avatar_hash is None:
			self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

	def __repr__(self):
		return '<User %r>' % (self.username)


class Tweet(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(300))
	timestamp = db.Column(db.DateTime)
	hearts = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	comments = db.relationship('Comment', backref='tweet', lazy='dynamic')

	def __repr__(self):
		return '<Tweet %r>' % (self.body)

class Comment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(300))
	timestamp = db.Column(db.DateTime)
	tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'))
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Comment %r>' % (self.body)


		