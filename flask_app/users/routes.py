from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flask_app import db, bcrypt
from flask_app.models import User, Project
from flask_app.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask_app.main.forms import SearchForm
from flask_app.users.utils import save_picture, send_reset_email

users = Blueprint("users", __name__)

@users.route("/register", methods = ["GET", "POST"])
def register():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    if current_user.is_authenticated:
        return redirect(url_for("main.browse"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username = form.username.data, email = form.email.data,
            name = form.name.data, password = hashed_pw)

        db.session.add(user)
        db.session.commit()

        flash(f"Account created for {form.username.data}, please login below.", "success")
        # Second one in flash is a class that can be used w/ CSS #
        return redirect(url_for("users.login"))

    return render_template("register.html", title = "Register", form = form, search_form = search_form)

@users.route("/login", methods = ["GET", "POST"])
def login():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    if current_user.is_authenticated:
        return redirect(url_for("main.browse"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.browse"))
        else:
            flash(f"Login unsuccessful", "failure")
    return render_template("login.html", title = "Login", form = form, search_form = search_form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.browse"))

@users.route("/account", methods = ["GET", "POST"])
@login_required
def account():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.name = form.name.data
        db.session.commit()
        flash(f"Your account has been updated.", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.name.data = current_user.name
    profile_pic = url_for("static", filename = "images/profile_pics/" + current_user.image_file)
    return render_template("account.html", title = "Account", profile_pic = profile_pic, form = form, search_form = search_form)

@users.route("/a/<string:username>", methods = ["GET", "POST"])
def user_projects(username):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    page = request.args.get("page", 1, type = int)
    user = User.query.filter_by(username = username).first_or_404()
    projects = Project.query.filter_by(author = user).order_by(Project.date_created.desc()).paginate(page = page, per_page = 5)
    return render_template("user_projects.html", title = "Author projects", projects = projects, user = user, search_form = search_form)

@users.route("/reset_password", methods = ["GET", "POST"])
def reset_request():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    if current_user.is_authenticated:
        return redirect(url_for("main.browse"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash(f"An email has been sent with instructions to reset your password.")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", form = form, title = "Password Reset", search_form = search_form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    if current_user.is_authenticated:
        return redirect(url_for("main.browse"))
    user = User.verify_reset_token(token)
    if user is None:
        flash(f"That is an invalid or expired token")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")

        user.password = hashed_pw
        db.session.commit()

        flash(f"Your password has been updated. You are now able to login.", "success")
        # Second one in flash is a class that can be used w/ CSS #
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", form = form, title = "Password Reset", search_form = search_form)
