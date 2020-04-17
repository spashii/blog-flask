from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from blog_flask.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
moment = Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    from blog_flask.main.routes import main
    app.register_blueprint(main)

    from blog_flask.posts.routes import posts
    app.register_blueprint(posts)

    from blog_flask.users.routes import users
    app.register_blueprint(users)

    from blog_flask.errors.handlers import errors
    app.register_blueprint(errors)
    
    return app


            

        