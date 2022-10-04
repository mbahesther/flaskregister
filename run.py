from  models import *
from passlib.hash import pbkdf2_sha256 as sha256
from extension.forget_maill import forget
from werkzeug.utils import secure_filename
import jwt as JWTT

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
            mail= send_mail(forms.email.data)
                   
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

@app.route('/download_home')
def download_home():    
       return render_template('download.html', title='download')

#download route
@app.route('/download')
def download():
       p = "hey.jpg"
       
       return send_file(p,as_attachment=True)
       #return send_file('innocent.docx',as_attachment=True)

def check_file_extension(filename):
   return filename.split('.')[-1] in allowed_extensions


#uploading the file
@app.route('/upload', methods=['GET', 'POST'])       
def upload():
   return render_template('upload.html', title='upload')


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
    file = request.files['file']
    if check_file_extension(file.filename):
      file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))    
      return 'file upload sucessfully'
    else:
      return "The file extension is not allowed"
   


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
         send= forget(forms.email.data)         
         flash('A link is sent to your email use it to reset password  and then login', 'info')
         return redirect(url_for('home'))
    return render_template('reset_request.html', title='Reset Password', forms=forms)




#to verify the token and also reset the password
@app.route('/passwordreset/<token>', methods=['GET','POST'])
def passwordreset(token):
    
    forms=ResetPasswordForm()
    verify=  JWTT.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
    
    print(verify)
    if verify is None:
        return('token expired or tampared go generate a new token to reset your password')
    else:
        email = verify['sub']    
        if forms.validate_on_submit():
            password =forms.password.data
            c_password = forms.c_password.data
            if password == c_password:
                  hash_password = sha256.hash(forms.password.data)
                  my_cursor.execute(f"""UPDATE user_register SET password=%s WHERE email = %s""", [hash_password, email])
               
                  mydb.commit()  
                  flash('your password has been updated! You can now login with the new password', 'success')
                  return redirect(url_for('login'))
     
    return render_template('reset_token.html', title='Reset Password', forms=forms)


from api import *

if __name__ == '__main__':
   app.run(debug=True)

#next_page = request.args.get('next')redirect(next_page) if next_page else