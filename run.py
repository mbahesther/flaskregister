from  models import *
from passlib.hash import pbkdf2_sha256 as sha256

# home route
@app.route('/')
def home():
   
   return render_template('home.html', title='home')

#register route
@app.route('/register', methods=['GET', 'POST'])
def register():
   forms = RegisterForm()
   if forms.validate_on_submit():
      email =forms.email.data
      password =forms.password.data
      c_password= forms.password.data 
      
      my_cursor.execute("""SELECT * FROM user_register WHERE email = %s""", [email])
      acc = my_cursor.fetchone()
      
      if acc:
         flash("Email already exists.", 'danger')
         return redirect(url_for('register'))
      else:
         if password == c_password:
            hash_password = sha256.hash(forms.password.data)
            my_cursor.execute('INSERT INTO user_register(firstname, lastname, email, password) VALUES (%s, %s, %s,%s)', (forms.firstname.data, forms.lastname.data, forms.email.data, hash_password ))
            mydb.commit()   
            #mail= send_mail(forms.email.data)
                   
            flash("Welcome,account created you can login and a message is sent to your email address",'success')
            return redirect(url_for('login') )
      
   return render_template('register.html', title="register", forms=forms)

      #    mail= send_mail(forms.email.data)
      
@app.before_request
def before_request():
  
   if 'user' in session:
      users =[x for x in 'user' if x == session['user']]
      g.users = session['user']
    

#login route
@app.route('/login', methods=['GET','POST'])
def login():
   forms = Loginform()
   if forms.validate_on_submit():
      email = forms.email.data
      my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
      my_cursor.execute("""SELECT * FROM user_register WHERE email = %s """, [email] ) #to database if the email exists
      user = my_cursor.fetchone()
   
      if user and sha256.verify(forms.password.data, user[4]):
            names ={
               'firstname': user[1],
               'lastname': user[2],
               'email': user[3]
            }
            session['user'] = names
            return redirect(url_for('dashboard'))
      else:
           flash("login unsuccessful, please enter correct email and password", 'danger')
           return redirect(url_for('login'))   
   return render_template('login.html', title ="login", forms=forms)


#dashboard route to
@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    
    forms = UpdateAccountForm()  
     
    return render_template('dashboard.html', title='dashboard', forms=forms)


#logout route
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))
  

#passsword reset route
@app.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:   
       return redirect(url_for('home'))
    forms = RequestResetForm()
    if forms.validate_on_submit():
      email = forms.email.data
      my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
      my_cursor.execute("""SELECT * FROM user_register WHERE email = %s """, [email] )
      user = my_cursor.fetchone()
      #user = UserRegister.query.filter_by(email=forms.email.data).first()  #checking if there is account with the email entered for the password request
      if user is None:
       flash('There is no account with that email, you must register first', 'danger')
      else:
         forget_passwordmail(user)
         
         
         flash('An email has been sent click on the link to reset your password', 'info')
         return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', forms=forms)

#for token route
@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:  
       return redirect(url_for('home'))
    my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
     
    user = my_cursor.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expire token', 'warning')
        return redirect(url_for('reset_request'))
    forms=ResetPasswordForm()
    if forms.validate_on_submit():
      password =forms.password.data
      c_password = forms.c_password.data
      if password == c_password:
            hash_password = sha256.hash(forms.password.data)
            my_cursor.execute('UPDATE INTO user_register(password) VALUES (%s)', (hash_password))
            mydb.commit()  
            flash('your password has been updated! You can now login with the new password', 'success')
            return redirect(url_for('login'))
      #  hashed_password = bcrypt.generate_password_hash(forms.password.data).decode('utf-8')
      #  user.password = hashed_password
      #  db.session.commit()
      
    return render_template('reset_token.html', title='Reset Password', forms=forms)




if __name__ == '__main__':
   app.run(debug=True)

#next_page = request.args.get('next')redirect(next_page) if next_page else