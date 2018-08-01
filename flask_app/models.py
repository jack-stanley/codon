from flask_app import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return User.query.get((int(user_id)))

class User(db.Model, UserMixin):
    __searchable__ = ["username", "name"]

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    email = db.Column(db.String(200), unique = True, nullable = False)
    name = db.Column(db.String(60), nullable = True)
    organization = db.Column(db.String(160), nullable = True)
    about = db.Column(db.Text, nullable = True)
    image_file = db.Column(db.String(20), nullable = False, default = "default_pic.jpg")
    password = db.Column(db.String(60), nullable = False)
    articles = db.relationship("Article", backref = "author", lazy = True)
    projects = db.relationship("Project", backref = "author", lazy = True)

    def get_reset_token(self, expires_sec = 1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.name}', '{self.image_file}')"

class Project(db.Model):
    __searchable__ = ["project_title", "abstract"]

    id = db.Column(db.Integer, primary_key = True)
    project_title = db.Column(db.String(400), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable = True)
    abstract = db.Column(db.Text, nullable = False)
    articles = db.relationship("Article", backref = "overall_project", lazy = True)
    headings = db.relationship("Heading", backref = "overall_project", lazy = True)
    tags = db.relationship("Tag", backref = "overall_project", lazy = True)
    banner_image = db.Column(db.String(20), nullable = False, default = "default_banner.png")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)

    def __repr__(self):
        return f"Project('{self.project_title}', '{self.date_created}')"

class Article(db.Model):
    __searchable__ = ["title", "content"]

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(400), nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    date_edited = db.Column(db.DateTime, nullable = True)
    content = db.Column(db.Text, nullable = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable = False)
    heading_id = db.Column(db.Integer, db.ForeignKey("heading.id"), nullable = False)

    def __repr__(self):
        return f"Article('{self.title}', '{self.date_posted}')"

class Heading(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    heading = db.Column(db.String(100), nullable = False, default = "Other")
    order = db.Column(db.Integer, nullable = False, default = "100")
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable = False)
    articles = db.relationship("Article", backref = "header", lazy = True)

    def __repr__(self):
        return f"Heading('{self.heading}')"

class Tag(db.Model):
    __searchable__ = ["tag"]

    id = db.Column(db.Integer, primary_key = True)
    tag = db.Column(db.String, nullable = False)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), nullable = False)
