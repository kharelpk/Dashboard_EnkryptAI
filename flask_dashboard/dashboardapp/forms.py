from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from dashboardapp.dbmodels import User
from flask_login import current_user

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

    # Validate the email, will error out directly in the form
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

      
# Create a registration form 
class LoginForm(FlaskForm):
    # Email
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    # Password: min 8, maximum length 50
    password = PasswordField('Password',validators=[DataRequired()])             
    remember = BooleanField('Remember Me')
    submit =SubmitField('Login')


# Create a registration form 
class UpdateAccountForm(FlaskForm):
   
    # Name fields: data input is required
    firstname = StringField('First name', 
                            validators=[DataRequired()])
    
    lastname = StringField('Last name', 
                            validators=[DataRequired()])

    # Email
    email = StringField('Email',
                        validators=[DataRequired(), Email()])

    submit =SubmitField('Update')

    # Validate the email, will error out directly in the form
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')
