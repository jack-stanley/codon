from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_app.config import Config
from flask_msearch import Search
from wtf_tinymce import wtf_tinymce

############
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "failure"
mail = Mail()

############
def create_app(config_class = Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    search = Search()
    search.init_app(app)
    wtf_tinymce.init_app(app)

    from flask_app.users.routes import users
    from flask_app.articles.routes import articles
    from flask_app.projects.routes import projects
    from flask_app.main.routes import main
    from flask_app.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(articles)
    app.register_blueprint(projects)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
