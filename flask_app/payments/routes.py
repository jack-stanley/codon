from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_app.models import User
from flask_app.payments.forms import CardForm
from flask_app import db
from flask_app.config import Config
import stripe, requests, json

payments = Blueprint("payments", __name__)

stripe.api_key = "sk_test_dZBIm0mCoNKvRb3P503B2sE2"

@payments.route("/payment_options")
@login_required
def payment_options():
    if current_user.customer_id:
        flash(f"Please go to your accounts page to manage payment options.")
        abort(403)
    return render_template("payment_options.html", title = "Enable crowdfunding?")

@payments.route("/record_fundraiser")
@login_required
def record_fundraiser():
    fundraiser_auth = request.args.get("code")
    data = {
            "client_secret": Config.CLIENT_SECRET,
            "code": fundraiser_auth,
            "grant_type": "authorization_code"
    }

    response = requests.post("https://connect.stripe.com/oauth/token", data)
    fundraiser_id = response.json().get("stripe_user_id")
    fundraiser_refresh = response.json().get("refresh_token")
    fundraiser_access = response.json().get("access_token")

    if fundraiser_id:
        current_user.fundraiser_id = fundraiser_id
        current_user.fundraiser_refresh = fundraiser_refresh
        current_user.fundraiser_access = fundraiser_access
        db.session.commit()
        flash(f"Your fundraiser account has been successfully connected.")
    else:
        flash(f"Fundraiser account not connected.")

    return redirect(url_for("users.account"))

@payments.route("/add_card", methods = ["GET", "POST"])
@login_required
def add_card():
    form = CardForm()
    if form.card_token.data:
        card_token = form.card_token.data
        if current_user.customer_id:
            card_token = form.card_token.data
            customer = stripe.Customer.retrieve(current_user.customer_id)
            customer.sources.create(source = card_token)
        else:
            customer = stripe.Customer.create(
                source = card_token,
                email = current_user.email
            )
            current_user.customer_id = customer.id
            db.session.commit()
        flash(f"Your card has been successfully added to your account.")
        return redirect(url_for("users.account"))
    return render_template("add_card.html", title = "Add card", form = form)

@payments.route("/delete_card/<card_id>")
@login_required
def delete_card(card_id):
    customer = stripe.Customer.retrieve(current_user.customer_id)
    customer.sources.retrieve(card_id).delete()
    flash(f"Your card has been successfully deleted.")
    return redirect(url_for("users.account"))

@payments.route("/default_card/<card_id>")
@login_required
def default_card(card_id):
    customer = stripe.Customer.retrieve(current_user.customer_id)
    customer.default_source = card_id
    customer.save()
    flash(f"Your card settings have been updated.")
    return redirect(url_for("users.account"))

@payments.route("/disconnect_stripe")
@login_required
def disconnect_stripe():
    current_user.fundraiser_id = None
    current_user.fundraiser_refresh = None
    current_user.fundraiser_access = None
    db.session.commit()
    flash(f"Your Stripe account has been successfully disconnected.")
    return redirect(url_for("users.account"))
