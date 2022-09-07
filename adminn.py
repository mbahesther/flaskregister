from lets import *
from passlib.hash import pbkdf2_sha256 as sha256


@app.route('/adminn', methods=['GET','POST'])

def adminn():
      forms=Adminform()
      if forms.validate_on_submit():
         email = forms.email.data
       
         my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
         my_cursor.execute("""SELECT * FROM admin WHERE email = %s """, [email]) #to database if the email exists
         user = my_cursor.fetchone()
         if user and sha256.verify(forms.password.data, user[2]):
         

               return redirect(url_for('admininfo'))
         else:
            flash("login unsuccessful, please enter correct email and password", 'danger')
            return redirect(url_for('adminn'))
      return render_template('admin.html', title='admin ', forms=forms)
  

@app.route('/admininfo')
def admininfo():  
    my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
    my_cursor.execute("SELECT * FROM user_register  ")
    rows =[]
    for row in my_cursor:
      rows.append(row)
      # print(row)

      
    return render_template('admininfo.html', title='admin', rows=rows)





 


if __name__ == '__main__':
   app.run(debug=True)