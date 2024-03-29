import os
import secrets
from PIL import Image, ImageOps
from flask import url_for, current_app
from flask_app.models import Tube, Project, User
from flask_app import db
from flask_login import current_user, login_required

def save_banner(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/images/project_pics", picture_fn)
    i = Image.open(form_picture)
    i.save(picture_path)
    return picture_fn
