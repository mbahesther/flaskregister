#first api testing
# get number and mutiplying by two
@app.route('/index', methods=['POST'])
def index():
    data = request.json
    print(data['number'])
    val = data['number'] * 2
    return {"msg":"logged in", "value":val}

#checking if my email exist in the database 
@app.route('/email', methods=['POST'])
def email():
    my_cursor = mydb.cursor(MySQLdb.cursors.DictCursor)
    data = request.json
    email = data['email']
    my_cursor.execute("""SELECT * FROM user_register WHERE email = %s """, [email] )
    check = my_cursor.fetchone()
    print(email)
    if check:
        return {"email": "email is in the database"}
    else:
       return {"email": "email doesnt exist"}
     

