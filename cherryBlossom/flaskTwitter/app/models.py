from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(16), index=True, unique=True)
	password_hash = db.Column(db.String(128), index=True)
	fName = db.Column(db.String(30), index=True)
	lName = db.Column(db.String(30), index=True)
	email = db.Column(db.String(120), index=True, unique=True)
	tweets = db.relationship('Tweet', backref='author', lazy='dynamic')
	
	@hybrid_property
	def password(self):
		return self.password_hash

	@password.setter
	def _set_password(self, plaintext):
		self.password_hash = bcrypt.generate_password_hash(plaintext)

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

	def __repr__(self):
		return '<User ' + self.username + '>'

class Tweet(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(140))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return '<Tweet ' + self.body + '>'


		