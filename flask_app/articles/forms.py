from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Optional
from wtf_tinymce.forms.fields import TinyMceField

class ArticleForm(FlaskForm):
    title = StringField("Title", validators = [DataRequired()])
    content = TinyMceField("Content (autosaves every 10 seconds)", tinymce_options = {"plugins": "autosave fullscreen hr preview insertdatetime code link print searchreplace pagebreak textcolor wordcount", "width": "80%", "autosave_interval": "10s", "menubar": "file edit format view insert tools",
    "toolbar": "undo redo | styleselect forecolor backcolor | fontselect fontsizeselect | bold italic underline strikethrough | alignleft, aligncenter, alignright, alignjustify | bullist, numlist, outdent, indent, blockquote | fullscreen preview", "browser_spellcheck": True})
    heading = StringField("Section")
    heading_order = IntegerField("Section order (eg. 3 is the 3rd section)", validators = [Optional()])
    submit = SubmitField("Post")
