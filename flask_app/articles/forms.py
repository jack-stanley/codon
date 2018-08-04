from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional, Length
from wtf_tinymce.forms.fields import TinyMceField

class ArticleForm(FlaskForm):
    title = StringField("Title", validators = [DataRequired(), Length(max  = 200)])
    content = TinyMceField("Content (autosaves every 10 seconds)", tinymce_options = {"plugins": "autosave fullscreen hr preview insertdatetime code link print searchreplace pagebreak textcolor wordcount", "width": "80%", "autosave_interval": "10s", "menubar": "file edit format view insert tools",
    "toolbar": "undo redo | styleselect forecolor backcolor | fontselect fontsizeselect | bold italic underline strikethrough | alignleft, aligncenter, alignright, alignjustify | bullist, numlist, outdent, indent, blockquote | fullscreen preview", "browser_spellcheck": True})
    section = SelectField("Section", choices = [("Introduction", "Introduction"), ("Main", "Main"), ("Resources", "Resources"), ("Miscellaneous", "Miscellaneous")])
    submit = SubmitField("Post")
