from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, BooleanField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, NumberRange, Length
from flask_login import current_user
import stripe

class CardForm(FlaskForm):
    card_token = StringField("")
    card_name = StringField("Name on card,*", validators = [DataRequired()])
    address = StringField("Address*", validators = [DataRequired()])
    city = StringField("City*", validators = [DataRequired()])
    province = StringField("Province/State*", validators = [DataRequired()])
    country = StringField("Country*", validators = [DataRequired()])
    submit = SubmitField("Add card")

class DonateForm(FlaskForm):
    amount = DecimalField("Contribution amount*", validators = [DataRequired(), NumberRange(min = 2, max = 1000)], places = 2)
    confirm_amount = DecimalField("Confirm contribution amount*", validators = [DataRequired(), EqualTo("amount"), NumberRange(min = 2, max = 1000)], places = 2)
    card = SelectField("Choose a card*")
    submit = SubmitField("Donate")

class ConfirmDonateForm(FlaskForm):
    password = PasswordField("Password", validators = [DataRequired(), Length(min = 5)])
    submit = SubmitField("Confirm donation")
