import email_validator
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import Email, DataRequired, Length, EqualTo, ValidationError
from instahelper_app.models import db, User

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=3, max=16)], description="Username")
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Account')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(f"{username.data} is in use with another member. Please choose different one.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(f"{email.data} is belongs to another member. Please use another email address.")

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=24)])
    submit = SubmitField('Confirm')

class HashtagForm(FlaskForm):
    hashtags = TextAreaField('Hashtags', validators=[Length(min=0, max=500)])
    like = BooleanField('Like Posts')
    comment = BooleanField('Send Comment to Posts')
    follow = BooleanField('Follow Owner')
    submit = SubmitField('Start Bot')

class ProfilePostsForm(FlaskForm):
    usernames = TextAreaField('Usernames', validators=[Length(min=0, max=500)])
    like = BooleanField('Like Posts')
    comment = BooleanField('Send Comment to Posts')
    follow = BooleanField('Follow Owner')
    submit = SubmitField('Start Bot')