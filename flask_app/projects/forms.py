from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class ProjectForm(FlaskForm):
    project_title = StringField("Project name", validators = [DataRequired()])
    summary = TextAreaField("Project summary (2000 characters max.)", validators = [DataRequired(), Length(max = 2000)])
    tags = StringField("Tags (separated by comma)", validators = [DataRequired()])
    submit = SubmitField("Post")
