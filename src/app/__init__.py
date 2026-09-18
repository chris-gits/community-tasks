import flask as Flask
import flask_bootstrap as FlaskBootstrap
import sqlalchemy as SQLAlchemy
import flask_sqlalchemy as FlaskSQLAlchemy
import flask_login as FlaskLogin
import flask_bcrypt as FlaskBCrypt
import flask_migrate as FlaskMigrate
import dotenv as DotENV
import os as OS

database = FlaskSQLAlchemy.SQLAlchemy()

def create_app():
    app = Flask.Flask(__name__, template_folder="templates")
    
    bootstrap = FlaskBootstrap.Bootstrap5(app)
    
    DotENV.load_dotenv()
 
    app.config['SQLALCHEMY_DATABASE_URI'] = OS.environ.get("DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = OS.environ.get("SECRET_KEY")
    
    database.init_app(app)
    
    from .models.users import User
    from .models.tasks import Task
    
    with app.app_context() as context:
        database.create_all()
    
    login_manager = FlaskLogin.LoginManager()
    login_manager.init_app(app)
    @login_manager.user_loader
    def load_user(user_id: int):
        return User.query.get(user_id)
    
    bcrypt = FlaskBCrypt.Bcrypt(app)
    
    from .routes import register_routes
    register_routes(app, database, bcrypt)
    
    migrate = FlaskMigrate.Migrate(app, database)
    
    return app