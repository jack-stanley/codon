from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired, Optional, Length
from wtf_tinymce.forms.fields import TinyMceField
from flask_wtf.recaptcha import RecaptchaField

class ArticleForm(FlaskForm):
    title = StringField("Title*", validators = [DataRequired(), Length(max  = 200)])
    content = TinyMceField("Content (autosaves every 10 seconds)", tinymce_options = {"plugins": "autosave fullscreen hr preview insertdatetime code link print searchreplace pagebreak textcolor wordcount image contextmenu table autolink", "width": "80%", "autosave_interval": "10s", "menubar": "file edit format view insert table tools",
    "toolbar": "undo redo | styleselect forecolor backcolor | fontsizeselect | bold italic underline strikethrough | alignleft, aligncenter, alignright, alignjustify | bullist, numlist, outdent, indent, blockquote | fullscreen preview", "browser_spellcheck": True, "contextmenu": "true copy cut paste | link image inserttable | cell row column deletetable",
    "content_css": "content.css", "body_class": "content_editor", "image_caption": True})
    section = SelectField("Section*", choices = [("Introduction", "Introduction"), ("Methods and Materials", "Methods and Materials"), ("Results", "Results"), ("Discussion and Conclusion", "Discussion and Conclusion"), ("Resources", "Resources"), ("References", "References"), ("Miscellaneous", "Miscellaneous")])
    submit = SubmitField("Post")
