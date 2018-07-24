from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length

class ProjectForm(FlaskForm):
    project_title = StringField("Project name", validators = [DataRequired(), Length(max = 100)])
    abstract = TextAreaField("Project abstract (2000 characters max.)", validators = [DataRequired(), Length(max = 2000)])
    tags = StringField("Tags (separated by comma)", validators = [DataRequired()])
    banner_image = FileField("Add project image", validators = [FileAllowed(["jpg", "png"])])
    submit = SubmitField("Create")
