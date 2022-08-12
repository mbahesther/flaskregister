from lets import *
 # user registration model
@login_manager.user_loader
def load_user(id):
   return UserRegister.query.get(int(id))

class UserRegister(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname =db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20),  nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password =db.Column(db.String(60), nullable= False)
    
    def get_reset_token(self, expires_sec=1800):
      s = Serializer(app.config['SECRET_KEY'], expires_sec)
      return s.dumps({'id': self.id}).decode('utf-8')
      

    @staticmethod
    def verify_reset_token(token):
      s =  Serializer(app.config['SECRET_KEY'])
      try:
         id = s.loads(token)['id']
        
      except Exception as e:
        
         return None
      
      return UserRegister.query.get(id)


    def __repr__(self):
        return f" UserRegister('{self.firstname}', '{self.lastname}', '{self.email}', '{self.password}')"

#creating a connection cursor
# cursor = mysql.connection.cursor()

# cursor.execute(''' INSERT INTO user_register(firstname, lastname, email, password)
#                VALUES('firstname','lastname') ''')
