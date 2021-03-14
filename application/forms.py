import email
from flask.app import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import validators
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from application.models import User


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember_me = BooleanField(label='Remember me')
    submit = SubmitField(label='Sign In')


class RegistrationForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    username = StringField(label='Username', validators=[DataRequired()])
    password1 = PasswordField(label='Password', validators=[DataRequired()])
    password2 = PasswordField(label='Reenter Password', validators=[
                              DataRequired(), EqualTo('password1')])
    submit = SubmitField(label='Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class RequestPasswordResetForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    submit = SubmitField(label="Request Password Reset")


class ResetPasswordForm(FlaskForm):
    password1 = PasswordField(label="Enter Password",
                              validators=[DataRequired()])
    password2 = PasswordField(
        label="Re-enter Password", validators=[DataRequired(), EqualTo('password1')])
    submit = SubmitField(label="Reset Password")
