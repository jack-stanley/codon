from flask import render_template, request, Blueprint, url_for, redirect
from flask_app.models import Project, Article, User
from flask_app.main.forms import SearchForm

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
    projects = Project.query.order_by(Project.date_created.desc()).paginate(page = page, per_page = 20)
    return render_template("browse.html", search_form = search_form, title = "Browse", projects = projects)

@main.route("/search/<string:search_query>/<string:search_type>", methods = ["GET", "POST"])
def search(search_query, search_type):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
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

    # tags = .....
