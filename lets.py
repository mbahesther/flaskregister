from flask import Flask, render_template, flash, redirect, url_for, session, request, g, send_file
from form import RegisterForm, Loginform, UpdateAccountForm, Adminform, RequestResetForm, ResetPasswordForm
from flask_sqlalchemy import SQLAlchemy
#from flask_bcrypt import Bcrypt
from extension.maill import send_mail

from flask_login import LoginManager, current_user, login_user, logout_user, login_required
#from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os
import MySQLdb.cursors
import mysql.connector


app = Flask(__name__)
    
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
#app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///registration.db'
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:''@localhost/our_flask'
app.config['UPLOAD_FOLDER'] = 'upload_folder/'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024    #size of the allowed file
allowed_extensions = ['jpg', 'png', 'jpeg']     #files extensions of the file allowed
#db = SQLAlchemy(app)
#bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'  #cant access the dashboard must login and take user to login route


mydb = mysql.connector.connect(
    host='localhost',
    user ='root',
    password ='',
    database ='our_flask',
  
    
)
my_cursor =mydb.cursor(buffered=True)

# my_cursor.execute("SHOW DATABASES")
# for db in my_cursor:
#     print(db)

# my_cursor.execute( '''CREATE TABLE IF NOT EXISTS user_register (
# 	id INT(11) NOT NULL AUTO_INCREMENT,
# 	firstname	VARCHAR(20) NOT NULL,
# 	lastname	VARCHAR(20) NOT NULL,
# 	email	VARCHAR(120) NOT NULL,
# 	password	VARCHAR(60) NOT NULL,
# 	PRIMARY KEY(id),
# 	UNIQUE(email)
# )
# ''')
# mydb.commit()
# my_cursor.execute( ''' 


# INSERT INTO user_register (id, firstname, lastname, email, password) VALUES (4,'om','om','omm@gmail.com','$2b$12$SsFC1fvffiamzzMJgvGF.e1G6p4z/2tAaCAjWYnBTVsgBqlCHYrpa');
# ''')
# mydb.commit()


 