from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp, Length

class UserSignUpForm(FlaskForm):
    first = StringField("First Name", validators = [DataRequired()])
    last = StringField("Last Name", validators = [DataRequired()])
    username = StringField("Username", validators = [DataRequired(), Regexp(r'^\w+$', message="Username must contain only letters, digits, or underscores")])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired(), Length(min=7, message="Password must be at least 7 characters long")])
    submit_button = SubmitField()

class UserSignInForm(FlaskForm):
    username = StringField("Username", validators = [DataRequired()])
    password = PasswordField("Password", validators = [DataRequired()])
    submit_button = SubmitField()