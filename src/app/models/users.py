from .. import database
import flask_login as FlaskLogin

class User(database.Model, FlaskLogin.UserMixin):
	__tablename__ = "users"
	
	id = database.Column(database.Integer, primary_key = True)
	name = database.Column(database.String, nullable = False, unique = True)
	email = database.Column(database.String, nullable = False, unique = True)
	password = database.Column(database.String, nullable = False)