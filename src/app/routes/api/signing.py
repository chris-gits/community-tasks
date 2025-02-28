import flask as Flask
import flask_login as FlaskLogin
from ... import models as Models


def register_routes(app, database, bcrypt):
    @app.route('/api/signup', methods=['POST'])
    def route_api_signup():
        form = Flask.request.form
        name = form.get('name')
        email = form.get('email')
        password = form.get('password')
        
        user = Models.users.User.query.filter_by(email=email).first()

        if user:
            Flask.flash("A user with that email already exists.", category="Warning")
            return Flask.redirect('/signup')
        
        try:
            new_user = Models.users.User(name=name, email=email, password=bcrypt.generate_password_hash(password))
            database.session.add(new_user)
            database.session.commit()
        except:
            Flask.flash("An error occurred whilst creating user. Please try again.", category="Danger")
            return Flask.redirect('/signup')
            
        
        FlaskLogin.login_user(new_user)
        Flask.flash("Successfully signed up.", category="Success")
        
        return Flask.redirect('/signin')
    
    @app.route('/api/signin', methods=['POST'])
    def route_api_signin():
        form = Flask.request.form
        
        email = form.get('email')
        password = form.get('password')
        print(email,password)		
        user = Models.users.User.query.filter_by(email=email).first()
        
        if not user or not bcrypt.check_password_hash(user.password, password):
            Flask.flash("Invalid credentials. Please try again.", category="Warning")
            return Flask.redirect('/signin')
        
        FlaskLogin.login_user(user)
        Flask.flash("Successfully signed in.", category="Success")
        
        return Flask.redirect('/signin')
    
    @app.route('/api/signout')
    def route_api_signout():
        FlaskLogin.logout_user()
        Flask.flash("Successfully signed out.", category="Success")
        return Flask.redirect('/signin')