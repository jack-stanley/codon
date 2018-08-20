from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, request
from flask_login import login_user, current_user, logout_user, login_required
from flask_app.models import User, Project
from flask_app.payments.forms import CardForm, DonateForm, ConfirmDonateForm
from flask_app import db, bcrypt
from flask_app.config import Config
import stripe, requests, json

payments = Blueprint("payments", __name__)

stripe_keys = {"secret_key": Config.CLIENT_SECRET, "public_key": Config.CLIENT_PUBLIC}

stripe.api_key = stripe_keys["secret_key"]

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
    if fundraiser_auth is None:
        abort(404)
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
    if form.validate_on_submit:
        if form.card_token.data:
            card_token = form.card_token.data
            if current_user.customer_id:
                card_token = form.card_token.data
                customer = stripe.Customer.retrieve(current_user.customer_id)
                card = customer.sources.create(source = card_token)
                card.address_line1 = form.address.data
                card.address_city = form.city.data
                card.address_state = form.province.data
                card.address_country = form.country.data
                card.name = form.card_name.data
                card.save()
            else:
                customer = stripe.Customer.create(email = current_user.email)
                card = customer.sources.create(source = card_token)
                card.address_line1 = form.address.data
                card.address_city = form.city.data
                card.address_state = form.province.data
                card.address_country = form.country.data
                card.name = form.card_name.data
                card.save()
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
    flash(f"Your card has been successfully removed from your account.")
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

@payments.route("/project/<int:project_id>/donate", methods = ["POST", "GET"])
@login_required
def donate(project_id):
    project = Project.query.get_or_404(project_id)
    form = DonateForm()
    if current_user == project.author:
        abort(403)
    if not (project.author.fundraiser_id and project.donations_goal):
        abort(404)
    if current_user.customer_id:
        customer = stripe.Customer.retrieve(current_user.customer_id)
        card_list = []
        for card in customer.sources:
            card_list.append((card.id, f"{card.brand} ending in {card.last4} ({card.exp_month}/{card.exp_year})"))
        card_list.append(("add_card", "Add new card"))
    else:
        card_list = [("add_card", "Add new card")]
    form.card.choices = card_list
    if form.submit.data and form.validate_on_submit():
        if form.card.data == "add_card":
            return redirect(url_for("payments.checkout_card", project_id = project.id, amount = form.amount.data))
        else:
            return redirect(url_for("payments.confirm_donate", card_id = form.card.data, project_id = project.id, amount = form.amount.data))

    return render_template("donate.html", title="Donate", form = form, project = project)

@payments.route("/project/<int:project_id>/donate/payment_method", methods = ["POST", "GET"])
@login_required
def checkout_card(project_id):
    project = Project.query.get_or_404(project_id)
    form = CardForm()
    amount = request.args.get("amount")

    if amount is None:
        abort(404)

    if current_user == project.author:
        abort(403)
    if not (project.author.fundraiser_id and project.donations_goal):
        abort(404)

    if form.validate_on_submit:
        if form.card_token.data:
            card_token = form.card_token.data
            if current_user.customer_id:
                card_token = form.card_token.data
                customer = stripe.Customer.retrieve(current_user.customer_id)
                card = customer.sources.create(source = card_token)
                card.address_line1 = form.address.data
                card.address_city = form.city.data
                card.address_state = form.province.data
                card.address_country = form.country.data
                card.name = form.card_name.data
                card.save()
            else:
                customer = stripe.Customer.create(email = current_user.email)
                card = customer.sources.create(source = card_token)
                card.address_line1 = form.address.data
                card.address_city = form.city.data
                card.address_state = form.province.data
                card.address_country = form.country.data
                card.name = form.card_name.data
                card.save()
                current_user.customer_id = customer.id
                db.session.commit()
            flash(f"Card added successfully")
            return redirect(url_for("payments.confirm_donate", project_id = project.id, card_id = card.id, amount = amount))

    return render_template("add_checkout_card.html", title = "Payment info", form = form)

@payments.route("/project/<int:project_id>/confirm_donate", methods = ["POST", "GET"])
@login_required
def confirm_donate(project_id):
    project = Project.query.get_or_404(project_id)
    card_id = request.args.get("card_id")
    if card_id is None:
        abort(404)
    customer = stripe.Customer.retrieve(current_user.customer_id)
    card = customer.sources.retrieve(card_id)
    if request.args.get("amount") is None:
        abort(404)
    amount = int(100 * float(request.args.get("amount")))
    codon_fees = int(0.06 * amount)
    form = ConfirmDonateForm()
    amount_display = float(amount / 100)

    token = stripe.Token.create(customer = current_user.customer_id, card = card, stripe_account = project.author.fundraiser_id)

    if current_user == project.author:
        abort(403)
    if not (project.author.fundraiser_id and project.donations_goal):
        abort(404)

    if form.submit.data and form.validate_on_submit:
        if bcrypt.check_password_hash(current_user.password, form.password.data):
            charge = stripe.Charge.create(amount = amount, currency = "usd", receipt_email = current_user.email, source = token.id, stripe_account = project.author.fundraiser_id, application_fee = codon_fees, description = f"Donation to {project.project_title}")
            flash(f"Thanks for your donation! A receipt will be sent to your email shortly!")
            project.donations_amount += amount_display
            db.session.commit()
            return redirect(url_for("projects.project", project_id = project.id))
        else:
            flash(f"Incorrect password", "failure")

    return render_template("confirm_donate.html", title = "Confirm donation", amount_display = amount_display, project = project, form = form, card = card)

@payments.route("/project/<int:project_id>/cancel_donation", methods = ["POST", "GET"])
@login_required
def cancel_donation(project_id):
    project = Project.query.get_or_404(project_id)
    if current_user == project.author:
        abort(403)
    if not (project.author.fundraiser_id and project.donations_goal):
        abort(404)
    flash(f"Donation cancelled.")
    return redirect(url_for("projects.project", project_id = project_id))
