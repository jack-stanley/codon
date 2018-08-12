from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_app import db, bcrypt
from flask_app.models import User, Project, Tube, Article, Tag
from flask_app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm, ChangePasswordForm, DeleteAccountForm
from flask_app.main.forms import SearchForm
from flask_app.users.utils import save_picture, send_reset_email, send_confirmation_email

users = Blueprint("users", __name__)

@users.route("/register", methods = ["GET", "POST"])
def register():
    search_form = SearchForm()
    if search_form.submit_search.data and search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    if current_user.is_authenticated:
        return redirect(url_for("main.browse"))
    form = RegistrationForm()
    if form.submit.data and form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user_old = User.query.filter_by(email = form.email.data).first()
        if user_old:
            db.session.delete(user_old)
            db.session.commit()
        user = User(username = form.username.data, email = form.email.data, name = form.name.data, organization = form.organization.data, password = hashed_pw)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("users.send_confirmation", user_id = user.id))

    return render_template("register.html", title = "Register", form = form, search_form = search_form)

@users.route("/login", methods = ["GET", "POST"])
def login():
    search_form = SearchForm()
    if search_form.submit_search.data and search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    if current_user.is_authenticated:
        return redirect(url_for("main.browse"))
    form = LoginForm()
    if form.submit.data and form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.confirmed == "True":
                login_user(user, remember = form.remember.data)
                next_page = request.args.get("next")
                return redirect(next_page) if next_page else redirect(url_for("main.browse"))
            else:
                return redirect(url_for("users.unconfirmed", user_id = user.id))
        else:
            flash(f"Login unsuccessful", "failure")
    return render_template("login.html", title = "Login", form = form, search_form = search_form)

@users.route("/unconfirmed/<user_id>", methods = ["GET", "POST"])
def unconfirmed(user_id):
    user = User.query.filter_by(id = user_id).first_or_404()
    if current_user.is_authenticated or user.confirmed == "True":
        return redirect(url_for("main.browse"))
    return render_template("unconfirmed.html", user = user, title = "Confirm email")

@users.route("/send_confirmation/<user_id>", methods = ["GET", "POST"])
def send_confirmation(user_id):
    user = User.query.filter_by(id = user_id).first_or_404()
    if current_user.is_authenticated or user.confirmed == "True":
        return redirect(url_for("main.browse"))
    send_confirmation_email(user)
    flash(f"A confirmation email has been sent with instructions to confirm your account.")
    return redirect(url_for("users.login"))

@users.route("/check_confirmation/<token>", methods = ["GET", "POST"])
def check_confirmation(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.browse"))
    user = User.verify_confirmation_token(token)
    if user is None:
        bob = bob
        flash(f"That is an invalid or expired token. Please register again if you cannot locate your confirmation email.")
        return redirect(url_for("users.register"))
    else:
        user.confirmed = "True"
        db.session.commit()
        flash(f"Your account has been confirmed. You are now able to login.", "success")
        return redirect(url_for("users.login"))


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.browse"))

@users.route("/account", methods = ["GET", "POST"])
@login_required
def account():
    search_form = SearchForm()
    if search_form.submit_search.data and search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    form = UpdateAccountForm()
    change_pass_form = ChangePasswordForm()
    delete_account_form = DeleteAccountForm()
    if form.submit.data and form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.name = form.name.data
        current_user.organization = form.organization.data
        current_user.about = form.about.data
        db.session.commit()
        flash(f"Your account has been updated.", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.name.data = current_user.name
        form.organization.data = current_user.organization
        form.about.data = current_user.about

    if change_pass_form.submit_change.data and change_pass_form.validate_on_submit():
        if current_user.email == change_pass_form.email.data:
            hashed_pw = bcrypt.generate_password_hash(change_pass_form.password.data).decode("utf-8")
            current_user.password = hashed_pw
            db.session.commit()
            flash(f"Your password has been changed.", "success")
            return redirect(url_for("users.account"))
        else:
            flash(f"Incorrect email entered.", "success")
            return redirect(url_for("users.account"))

    if delete_account_form.submit_delete.data and delete_account_form.validate_on_submit():
        if current_user.email == delete_account_form.email.data and current_user.username == delete_account_form.username.data and bcrypt.check_password_hash(current_user.password, delete_account_form.password.data):
            return redirect(url_for("users.delete_account", user_id = current_user.id))
        else:
            flash(f"Incorrect credentials entered.")
            return redirect(url_for("users.account"))

    profile_pic = url_for("static", filename = "images/profile_pics/" + current_user.image_file)
    return render_template("account.html", delete_account_form = delete_account_form, change_pass_form = change_pass_form, title = " | Account info", profile_pic = profile_pic, form = form, search_form = search_form)

@users.route("/a/<string:username>", methods = ["GET", "POST"])
def user_projects(username):
    search_form = SearchForm()
    if search_form.submit_search.data and search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    page = request.args.get("page", 1, type = int)
    user = User.query.filter_by(username = username).first_or_404()
    projects = Project.query.filter_by(author = user).order_by(Project.date_created.desc()).paginate(page = page, per_page = 5)
    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = None
    def toggle_colour(project_id, user_id):
        if Tube.query.filter_by(project_id = project_id, user_id = user_id).first() is not None:
            return "coloured"
        else:
            return ""
    def tube_count(project_id):
        if Tube.query.filter_by(project_id = project_id).all() is None:
            return 0
        else:
            return Tube.query.filter_by(project_id = project_id).count()
    return render_template("user_projects.html", tube_count = tube_count, toggle_colour = toggle_colour, user_id = user_id, title = f" | {user.username}", projects = projects, user = user, search_form = search_form)

@users.route("/reset_password", methods = ["GET", "POST"])
def reset_request():
    search_form = SearchForm()
    if search_form.submit_search.data and search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    if current_user.is_authenticated:
        return redirect(url_for("main.browse"))
    form = RequestResetForm()
    if form.submit.data and form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash(f"An email has been sent with instructions to reset your password.")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", form = form, title = "Password reset", search_form = search_form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    search_form = SearchForm()
    if search_form.submit_search.data and search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    if current_user.is_authenticated:
        return redirect(url_for("main.browse"))
    user = User.verify_reset_token(token)
    if user is None:
        flash(f"That is an invalid or expired token.")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.submit.data and form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        user.password = hashed_pw
        db.session.commit()

        flash(f"Your password has been updated. You are now able to login.", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", form = form, title = "Password reset", search_form = search_form)

@users.route("/delete_account/<user_id>")
def delete_account(user_id):
    user = User.query.get_or_404(user_id)
    articles = Article.query.filter_by(author = user)
    projects = Project.query.filter_by(author = user)
    tubes_user = Tube.query.filter_by(user_id = user_id)
    if user != current_user:
        abort(403)
    for article in articles:
        db.session.delete(article)
    for project in projects:
        tags = Tag.query.filter_by(overall_project = project)
        for tag in tags:
            db.session.delete(tag)
        tubes_project = Tube.query.filter_by(project_id = project.id)
        for tube in tubes_project:
            db.session.delete(tube)
        db.session.delete(project)
    for tube in tubes_user:
        db.session.delete(tube)
    db.session.delete(user)
    db.session.commit()
    flash(f"Your account and all related content has been deleted", "success")
    return redirect(url_for("main.browse"))
