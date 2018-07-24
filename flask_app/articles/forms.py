from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Optional

class ArticleForm(FlaskForm):
    title = StringField("Title", validators = [DataRequired()])
    content = TextAreaField("Content", validators = [DataRequired()])
    heading = StringField("Section")
    heading_order = IntegerField("Section order (eg. 3 is the 3rd section)", validators = [Optional()])
    submit = SubmitField("Post")
