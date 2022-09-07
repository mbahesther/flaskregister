from flask import Flask, request
from flask import jsonify
from lets import app, mydb, my_cursor
import MySQLdb.cursors
from passlib.hash import pbkdf2_sha256 as sha256

import os
import MySQLdb.cursors
import mysql.connector

from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user


jwt = JWTManager(app)


#creating a api route that signs up users
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    firstname = data['firstname']
    email = data['email']
    password = data['password']
    my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
    my_cursor.execute(""" SELECT * FROM  account WHERE  email = %s """,  [email])
    account = my_cursor.fetchone()
    if account:
        return { "email": "email is already registered choose a differnt email" }
    else :

        hash_password = sha256.hash(password)
        my_cursor.execute(' INSERT INTO account(firstname, email, password) VALUES (%s, %s, %s) ', (firstname, email, hash_password) )
        mydb.commit()
        return { "account": "your account has been created"}



#api sign in route
@app.route('/signin', methods=['POST'])
def signin():
     data = request.json
     email = data['email']
     password = data['password']
     my_cursor =  mydb.cursor(MySQLdb.cursors.DictCursor)
     my_cursor.execute("""SELECT * FROM account WHERE email = %s """, [email] ) #to database if the email exists
     acc = my_cursor.fetchone()
     if acc and sha256.verify(password, acc[3]):
       
         access_token = create_access_token(identity=acc)
         return jsonify(access_token=access_token)
        
     else:
       return jsonify("Wrong username or password"), 401
       #return  {"logged": "incorrect email or password "}


@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200



#passsword reset route
