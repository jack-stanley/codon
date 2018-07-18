from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flask_app.models import User

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(),
        Length(min = 2, max = 30)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    name = StringField("Name/Organization (optional)", validators = [Length(max = 60)])
    password = PasswordField("Password", validators = [DataRequired(),
        Length(min = 5)])
    confirm_password = PasswordField("Confirm Password",
        validators = [DataRequired(), Length(min = 5), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("That username is already taken.")

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("That email is used on another account.")

class LoginForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired(),
        Length(min = 5)])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Login")

class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired(),
        Length(min = 2, max = 30)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    name = StringField("Name/Organization (optional)", validators = [Length(max = 60)])
    picture = FileField("Update profile picture", validators = [FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError("That username is already taken.")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError("That email is used on another account.")

class RequestResetForm(FlaskForm):
    email = StringField("Email", validators = [DataRequired(), Email()])
    submit = SubmitField("Send Email")
    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError("There is no account with that Email. Please register first.")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators = [DataRequired(),
        Length(min = 5)])
    confirm_password = PasswordField("Confirm Password",
        validators = [DataRequired(), Length(min = 5), EqualTo("password")])
    submit = SubmitField("Reset Password")
