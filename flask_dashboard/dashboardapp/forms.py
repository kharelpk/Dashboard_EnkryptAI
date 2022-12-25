from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

# Create a registration form 
class RegistrationForm(FlaskForm):
   
    # Name fields: data input is required
    firstname = StringField('First name', 
                            validators=[DataRequired()])
    
    lastname = StringField('Last name', 
                            validators=[DataRequired()])

    # Email
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    # Password: min 8, maximum length 50
    password = PasswordField('Password',validators=[DataRequired(), Length(min=8, max=50)])             

    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), Length(min=8, max=50), EqualTo('password')])             

    submit =SubmitField('Sign up')

# Create a registration form 
class LoginForm(FlaskForm):
    # Email
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    # Password: min 8, maximum length 50
    password = PasswordField('Password',validators=[DataRequired()])             
    remember = BooleanField('Remember Me')
    submit =SubmitField('Login')