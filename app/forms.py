from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, PasswordField, IntegerField
from flask import flash
from app.models import User
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

class PostForm(FlaskForm):
    pic = FileField('Choose picture: ')
    desc = StringField('Tell me about this picture: ')
    submit = SubmitField('Post')

class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('E-mail:', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Re-type Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')

    # setup validation methods to be checked when form is submitted
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            flash('Sorry, but those credentials are already in use.')
            raise ValidationError('E-mail already taken.')

class RequestResetForm(FlaskForm):
    email = StringField('E-mail:', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Re-type Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')

class EditProfileForm(FlaskForm):
    bio = StringField('About me: ')
    pic = FileField()
    submit = SubmitField('Submit')

# , validators=[FileAllowed('jpg', 'png')]

# class UpdateInfoForm(FlaskForm):
#     username = StringField('Username:', validators=[DataRequired()])
#     email = StringField('E-mail:', validators=[DataRequired(), Email()])
#     age = IntegerField('Age:')
#     bio = StringField('Bio:')
#     url = StringField('Profile Pic URL:')
#     password = PasswordField('Password', validators=[DataRequired()])
#     password2 = PasswordField('Re-type Password', validators=[DataRequired(), EqualTo('password')])
#     submit = SubmitField('Register')
#
#     def validate_username(self, username):
#         user = User.query.filter_by(username=username.data).first()
#         if user is not None:
#             flash('Sorry, but those credentials are already in use.')
#             raise ValidationError('E-mail already taken.')
