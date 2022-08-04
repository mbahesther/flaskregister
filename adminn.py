
from lets import *
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from run import UserRegister

# app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///admin.db'
# db = SQLAlchemy(app)
#login_manager = LoginManager(app)
admin =Admin(app) 
admin.add_view(ModelView(UserRegister, db.session))

# @login_manager.user_loader
# def load_user(user_id):
#    return UserRegister.query.get(user_id)

# class User(db.Model, UserMixin):
#    id =db.Column(db.Integer, primary_key=True)
#    name= db.Column(db.String(20))
   

# class MyModelView(ModelView):
#    def is_accessible(self):
#       return current_user.is_authenticated

#    def inaccessible_callback(self, name, **kwargs):
#       return redirect(url_for('login'))

# class MyAdminIndexView(AdminIndexView):
#     def is_accessible(self):
#       return current_user.is_authenticated

# admin = Admin(app, index_view=MyAdminIndexView)
# admin.add_view(ModelView(User, db.session))

# @app.route('/login')
# def login():
#    user = UserRegister.query.get(1)
#    login_user(user)
#    return 'logged in'

# @app.route('/logout')
# def logout():
#    logout_user()
#    return 'logged out out'   



 


if __name__ == '__main__':
   app.run(debug=True)