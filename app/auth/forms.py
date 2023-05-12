from flask_wtf import FlaskForm
from ..models import User


from wtforms import (
    StringField,
    ValidationError,
    PasswordField,
    BooleanField,
    SubmitField,
    validators)


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired(message='Username is required')])
    password = PasswordField("Password", validators=[
                                         validators.DataRequired(message='Password is required'),
                                         validators.Length(min=6, message="Password should have at least 6 symbols")])
    remember = BooleanField("Remember")
    submit = SubmitField("Log In")


class RegisterForm(LoginForm):

    first_name = StringField("First name", validators=[validators.Optional()])
    last_name = StringField("Last name", validators=[validators.Optional()])
    email = StringField("Email", validators=[validators.DataRequired(message='Email is required'), validators.Email()])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[
                                         validators.DataRequired(message='Confirm password is required'),
                                         validators.EqualTo('password', message='Password should match')])
    submit = SubmitField("Sign up")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists')
