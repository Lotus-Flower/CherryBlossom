from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password_hash = PasswordField('password', validators=[DataRequired()])
	rememberMe = BooleanField('rememberMe')

class RegisterForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password_hash = PasswordField('password', validators=[DataRequired()])
	fName = StringField('fName', validators=[DataRequired()])
	lName = StringField('lName', validators=[DataRequired()])
	email = StringField('email', validators=[DataRequired()])

class TweetForm(Form):
	body = TextAreaField('body', validators=[DataRequired()])

class CommentForm(Form):
	body = TextAreaField('body', validators=[DataRequired()])

class SearchForm(Form):
	username = StringField('username', validators=[DataRequired()])