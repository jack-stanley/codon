from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, SubmitField, TextAreaField, ValidationError, PasswordField, DecimalField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, NumberRange, Optional
from flask_app.models import User

def check_unique(form, field):
    stripped = field.data.strip()
    split_list = stripped.split(", ")
    unique = []
    duplicate = []
    for item in split_list:
        if item not in unique:
            unique.append(item)
        else:
            duplicate.append(item)
    if duplicate != []:
        t = ""
        i = 0
        for item in duplicate:
            if i == 0:
                t = t + item
            elif len(duplicate) != 1:
                t = t + ", " + item
            i += 1
        raise ValidationError(f"Duplicates entered: {t}.")

def validate_collabs(form, field):
    stripped = field.data.strip()
    split_list = stripped.split(", ")
    error_list = []
    for username in split_list:
        if ((User.query.filter_by(username = username).first() is None) or username == current_user.username) and username != "":
            error_list.append(username)
    if error_list != []:
        t = ""
        for item in error_list:
            if item == error_list[0]:
                t = t + item
            elif tags_len != 1:
                t = t + ", " + item
        raise ValidationError(f"Invalid usernames entered: {t}.")

def limit_tags(form, field):
    stripped = field.data.strip()
    split_list = stripped.split(", ")
    if len(split_list) > 5:
        raise ValidationError(f"Too many tags entered, please only include 5 tags.")

class ProjectForm(FlaskForm):
    project_title = StringField("Project name*", validators = [DataRequired(), Length(max = 100)])
    abstract = TextAreaField("Project abstract*", validators = [DataRequired(), Length(max = 2000)])
    tags = StringField("Tags (5 max, comma separated)*", validators = [DataRequired(), limit_tags, check_unique])
    collaborators = StringField("Collaborators (valid usernames separated by comma)", validators = [validate_collabs, check_unique])
    donations_goal = DecimalField("Funding goal in USD (leave blank if you don't want donations)", validators = [Optional(), NumberRange(min = 100)], places = 2)
    banner_image = FileField("Add project image", validators = [FileAllowed(["jpg", "png"])])
    submit = SubmitField("Submit")

class DeleteProjectForm(FlaskForm):
    project_title = StringField("Project name", validators = [DataRequired(), Length(max = 100)])
    email = StringField("Email", validators = [DataRequired(), Email()])
    password = PasswordField("Password", validators = [DataRequired(), Length(min = 5)])
    submit_delete = SubmitField("DELETE")
