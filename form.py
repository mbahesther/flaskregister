from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length, Email, EqualTo



#register user form
class RegisterForm(FlaskForm):
    firstname = StringField ('First Name', validators = [DataRequired(), length(min=2, max=25)])
    lastname = StringField('Last name', validators = [DataRequired(), length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), length(min=6)])
    c_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')


 
          
#login form
class Loginform(FlaskForm):
        email = StringField('Email', validators=[DataRequired(), Email()])
        password =PasswordField('Password', validators=[DataRequired()])
        submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    firstname = StringField ('First Name', validators = [DataRequired(), length(min=2, max=25)])
    lastname = StringField('Last name', validators = [DataRequired(), length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    submit = SubmitField('Update')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Reset Password')
   


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), length(min=6)])
    c_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
