from flask import render_template, request, Blueprint, url_for, redirect
from flask_app.models import Project, Article, User, Tag, Tube
from flask_app.main.forms import SearchForm
from flask_login import current_user, login_required
from flask_app import db

main = Blueprint("main", __name__)

@main.route("/", methods = ["GET", "POST"])
def index():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    return render_template("index.html", search_form = search_form)


@main.route("/about", methods = ["GET", "POST"])
def about():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    return render_template("about.html", title = "About", search_form = search_form)

@main.route("/browse", methods = ["GET", "POST"])
def browse():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    page = request.args.get("page", 1, type = int)
    projects = Project.query.order_by(Project.date_edited.desc()).paginate(page = page, per_page = 20)
    user_id = current_user.id
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
    return render_template("browse.html", tube_count = tube_count, toggle_colour = toggle_colour, search_form = search_form, user_id = user_id, title = "Browse", projects = projects)

@main.route("/search/<string:search_query>/<string:search_type>", methods = ["GET", "POST"])
def search(search_query, search_type):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = search_type))
    else:
        search_form.search_query.data = search_query

    page = request.args.get("page", 1, type = int)

    if search_type == "project_search":
        projects = Project.query.msearch(f"{search_query}").paginate(page = page, per_page = 20)
        return render_template("search.html", search_query = search_query, search_type = search_type, search_form = search_form, projects = projects)
    if search_type == "article_search":
        articles = Article.query.msearch(f"{search_query}").paginate(page = page, per_page = 20)
        return render_template("search_article.html", search_query = search_query, search_type = search_type, search_form = search_form, articles = articles)
    if search_type == "user_search":
        users = User.query.msearch(f"{search_query}").paginate(page = page, per_page = 20)
        return render_template("search_user.html", search_query = search_query, search_type = search_type, search_form = search_form, users = users)
    if search_type == "tag_search":
        tags = Tag.query.filter_by(tag = search_query).paginate(page = page, per_page = 20)
        return render_template("search_tags.html", search_query = search_query, search_type = search_type, search_form = search_form, tags = tags)

@main.route("/tubes/<int:project_id>/<int:user_id>", methods = ["POST"])
@login_required
def tube_toggle(project_id, user_id):
    if current_user.id != user_id:
        abort(403)
    if Tube.query.filter_by(project_id = project_id, user_id = user_id).first() is None:
        tube = Tube(project_id = project_id, user_id = user_id)
        db.session.add(tube)
        db.session.commit()
    else:
        tube = Tube.query.filter_by(project_id = project_id, user_id = user_id).first()
        db.session.delete(tube)
        db.session.commit()
    return "5"
