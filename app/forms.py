from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError
from app.models import User


class RegistrasiForm(FlaskForm) :
	username = StringField('Username', validators=[DataRequired(), length(min=2, max=20)]) 
	password = PasswordField('Password', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Registrasi')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Masuk')

class PostForm(FlaskForm):
	isi = TextField('Isi', validators=[DataRequired()])
	submit = SubmitField('post')