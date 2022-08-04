from flask import Flask, render_template, flash, redirect, url_for,session, request
from form import RegisterForm, Loginform
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from extension.maill import send_mail
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user

#LoginManager to initialze our login, UserMixin suppose for the db in our model,
# login_user to log the user in


app = Flask(__name__)
    
app.config['SECRET_KEY'] = 'ae70b798854d82f9d79d91c347d8c4d2'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///registration.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)