from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    validators)



class LoginForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired(message='Username is required')])
    password = PasswordField("Password", validators=[validators.DataRequired(message='Password is required'),
               validators.Length(min=6, message="Password should have at least 6 symbols")])
    remember = BooleanField("Remember")
    submit = SubmitField("Log In")

class RegisterForm(LoginForm):
    email = StringField("Email", validators=[validators.DataRequired(message='Email is required'), validators.Email()])
    confirm_password = PasswordField("Confirm Password",
                                     validators=[validators.DataRequired(message='Confirm password is required'),
                                     validators.EqualTo('password', message='Password should match')])
    submit = SubmitField("Sign up")
