from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Optional, Length

class SearchForm(FlaskForm):
    search_query = StringField(validators = [DataRequired(), Length(max = 200)])
    submit_search = SubmitField("Search")
