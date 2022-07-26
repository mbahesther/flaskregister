
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length, Email, EqualTo




class RegisterForm(FlaskForm):
    firstname = StringField ('First Name', validators = [DataRequired(), length(min=2, max=25)])
    lastname = StringField('Last name', validators = [DataRequired(), length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), length(min=6)])
    c_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')


    #check for double email
    # def validate_email(self, email):
    #     user = UserRegister.query.filter_by(email=email.data).first()
    #     if user:
    #         raise ValidationError('email already exits')
          

class Loginform(FlaskForm):
        email = StringField('Email', validators=[DataRequired(), Email()])
        password =PasswordField('Password', validators=[DataRequired()])
        submit = SubmitField('Login')