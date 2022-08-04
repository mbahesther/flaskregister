from lets import *

 # user registration model
@login_manager.user_loader
def load_user(user_id):
   return UserRegister.query.get(int(user_id))

class UserRegister(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname =db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20),  nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password =db.Column(db.String(60), nullable= False)
    
    def __repr__(self):
        return f" UserRegister('{self.firstname}', '{self.lastname}', '{self.email}', '{self.password}')"



# home route
@app.route('/')
def home():
   return render_template('home.html', title='home')

#register route
@app.route('/register', methods=['GET', 'POST'])
def register():
 
   forms = RegisterForm()
   if forms.validate_on_submit():
      #to check if the email exit before registering the user
      if UserRegister.query.filter_by(email=forms.email.data).first():
         flash("Email already exists.", 'danger')
         return redirect(url_for('register'))
      hashed_password = bcrypt.generate_password_hash(forms.password.data).decode('utf-8')
      user = UserRegister(firstname=forms.firstname.data, lastname=forms.lastname.data,
       email=forms.email.data,
       password=hashed_password)
      db.session.add(user)
      db.session.commit()
      if user:
         mail= send_mail(forms.email.data)
      
      flash("Welcome,account created you can login and a message is sent to you",'success')
      

      return redirect(url_for('login'))
      
   return render_template('register.html', title="register", forms=forms)



#login route
@app.route('/login', methods=['GET','POST'])
def login():
   
   forms = Loginform()
   if forms.validate_on_submit():
      user = UserRegister.query.filter_by(email= forms.email.data).first()
      if user and bcrypt.check_password_hash(user.password, forms.password.data):
         login_user(user)
         #flash("You are logged in", 'success')
         return redirect(url_for('home'))
      else:
         flash("login unsuccessful, please enter correct email and password", 'danger')
         return redirect(url_for('login'))   
   return render_template('login.html', title ="login", forms=forms)



#logout route
@app.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('home'))

if __name__ == '__main__':
   app.run(debug=True)