import os
import secrets
from PIL import Image, ImageOps
from flask import url_for, current_app
from flask_mail import Message
from flask_app import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/images/profile_pics", picture_fn)
    i = Image.open(form_picture)
    width, height = i.size
    if width >= height:
        output_size = (width, 150)
    else:
        output_size = (150, height)
    i.thumbnail(output_size)
    width, height = i.size
    if width >= height:
        i_cropped = i.crop(((width - 150) / 2, 0, (width - 150) / 2 + 150, 150))
    else:
        i_cropped = i.crop((0, (height - 150) / 2, 150, (height - 150) / 2 + 150))
    i_cropped.save(picture_path)
    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Codon Password Reset", sender="noreply@codon.com", recipients = [user.email])
    msg.body = f"""To reset your password, please visit the following link:
    {url_for('users.reset_token', token = token, _external = True)}

    If you did not make this request, simply ignore this email."""

    mail.send(msg)
