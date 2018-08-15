from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class CardForm(FlaskForm):
    card_token = StringField("")
    submit = SubmitField("Add card")
