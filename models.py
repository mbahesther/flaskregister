
from flaskreg import db


# class UserRegister(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     firstname =db.Column(db.String(20), unique=True, nullable=False)
#     lastname = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password =db.Column(db.String(60), nullable= False)
    
#     def __repr__(self):
#         return f" UserRegister('{self.firstname}', '{self.lastname}', '{self.email}', '{self.password}')"
