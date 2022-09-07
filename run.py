from  models import *
from passlib.hash import pbkdf2_sha256 as sha256
from extension.forget_maill import forget_passwordmail, generateOTP

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
    session.pop('user', None)
    return redirect(url_for('login'))



from adminn import *

#passsword reset route
@app.route('/reset_password', methods=['GET','POST'])
def reset_request():
     
    forms = RequestResetForm()
    if forms.validate_on_submit():
      email = forms.email.data
      my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
      my_cursor.execute("""SELECT * FROM user_register WHERE email = %s """, [email] )
      user = my_cursor.fetchone()
      
      if user is None:
       flash('There is no account with that email, you must register first', 'danger')
      else:
         send= forget_passwordmail(forms.email.data)         
         flash('An opt  has been sent to your email, enter the opt ', 'info')
         return redirect(url_for('verify_otp'))
    return render_template('reset_request.html', title='Reset Password', forms=forms)


@app.route('/verify_otp', methods=['GET','POST'])
def verify_otp():
   forms= OtpForm()
   if forms.validate_on_submit():
      
      user_otp = forms.otp.data
      my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
      my_cursor.execute("""SELECT * FROM user_register WHERE otp = %s """, [user_otp] )
      opt = my_cursor.fetchone()
      if opt == user_otp:
          return redirect(url_for('reset_otp'))
      else:
         flash("Please check your otp and enter the correct otp")
   return render_template('otp.html', tittle='Otp verfication', forms=forms)


#for token route
@app.route('/reset_password/<token>', methods=['GET','POST'])
def reset_otp(otp):
    
   #  my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
   #  user = my_cursor.verify_reset_token(token)
   #  if user is None:
   #      flash('That is an invalid or expire token', 'warning')
   #      return redirect(url_for('reset_request'))
    forms=ResetPasswordForm()
    if forms.validate_on_submit():
      password =forms.password.data
      c_password = forms.c_password.data
      if password == c_password:
            hash_password = sha256.hash(forms.password.data)

            my_cursor.execute(f'UPDATE SET user_register(password) VALUES (%s) {hash_password} WHERE otp = {otp}')
            #my_cursor.execute(f'UPDATE account  SET password = {hash_password}  WHERE email = {email}' )

            mydb.commit()  
            flash('your password has been updated! You can now login with the new password', 'success')
            return redirect(url_for('login'))
      #  hashed_password = bcrypt.generate_password_hash(forms.password.data).decode('utf-8')
      #  user.password = hashed_password
      #  db.session.commit()
      
    return render_template('reset_token.html', title='Reset Password', forms=forms)


from api import *

if __name__ == '__main__':
   app.run(debug=True)

#next_page = request.args.get('next')redirect(next_page) if next_page else