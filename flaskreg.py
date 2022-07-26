from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from form import RegisterForm, Loginform


app = Flask(__name__)

app.config['SECRET_KEY'] = 'ae70b798854d82f9d79d91c347d8c4d2'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///registration.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class UserRegister(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname =db.Column(db.String(20), unique=True, nullable=False)
    lastname = db.Column(db.String(20),  nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password =db.Column(db.String(60), nullable= False)
    
    def __repr__(self):
        return f" UserRegister('{self.firstname}', '{self.lastname}', '{self.email}', '{self.password}')"


@app.route('/')
def home():
   return render_template('home.html', title='home')

@app.route('/register', methods=['GET', 'POST'])
def register():
    forms = RegisterForm()
    if forms.validate_on_submit():
      if UserRegister.query.filter_by(email=forms.email.data).first():
         flash("Email already exists.", 'danger')
         return redirect(url_for('register'))
      hashed_password = bcrypt.generate_password_hash(forms.password.data).decode('utf-8')
      user = UserRegister(firstname=forms.firstname.data, lastname=forms.lastname.data,
      email=forms.email.data, password=hashed_password)
      db.session.add(user)
      db.session.commit()
      flash("Welcome, account created you can login", 'success')
      return redirect(url_for('login'))
  
    return render_template('register.html', title="register", forms=forms)


@app.route('/login', methods=['GET','POST'])
def login():
   forms = Loginform()
   if forms.validate_on_submit():
      user = UserRegister.query.filter_by(email= forms.email.data).first()
      if user:

         flash("You are logged in", 'success')
         return redirect(url_for('home'))
      else:
         flash("login unsuccessful, please enter correct email and password", 'danger')
         return redirect(url_for('login'))   
   return render_template('login.html', title ="login", forms=forms)



if __name__ == '__main__':
   app.run(debug=True)