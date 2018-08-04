from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flask_app import db
from flask_app.models import Article, Project
from flask_app.articles.forms import ArticleForm
from flask_app.main.forms import SearchForm
from datetime import datetime

articles = Blueprint("articles", __name__)

def collab_user(project_id):
    project = Project.query.get_or_404(project_id)
    collabs = project.collaborators
    stripped = collabs.strip()
    split_tags_list = stripped.split(", ")
    return split_tags_list

@articles.route("/project/<int:project_id>/article/<int:article_id>", methods = ["GET", "POST"])
def article(article_id, project_id):
    search_form = SearchForm()
    if search_form.submit_search.data and search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    collabs = collab_user(project_id)
    project = Project.query.get_or_404(project_id)
    article = Article.query.get_or_404(article_id)
    return render_template("article.html", collabs = collabs, title = article.title, article = article, project = project, search_form = search_form)

@articles.route("/project/<int:project_id>/article/new", methods = ["GET", "POST"])
@login_required
def new_article(project_id):
    search_form = SearchForm()
    if search_form.submit_search.data and search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    form = ArticleForm()
    project = Project.query.get_or_404(project_id)
    if project.author != current_user and current_user.username not in collab_user(project_id):
        abort(403)
    if form.submit.data and form.validate_on_submit():
        article = Article(title = form.title.data, date_edited = datetime.utcnow(), content = form.content.data, section = form.section.data, overall_project = project, author = current_user)
        project.date_edited = datetime.utcnow()
        db.session.add(article)
        db.session.commit()
        flash(f"Your article has been created.")
        return redirect(url_for("articles.article", article_id = article.id, project_id = project.id))
    return render_template("create_article.html", form = form, legend = "Create Article", search_form = search_form)

@articles.route("/project/<int:project_id>/article/<int:article_id>/update", methods = ["GET", "POST"])
@login_required
def update_article(article_id, project_id):
    search_form = SearchForm()
    if search_form.submit_search.data and search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    project = Project.query.get_or_404(project_id)
    article = Article.query.get_or_404(article_id)
    if article.author != current_user and project.author != current_user and current_user.username not in collab_user(project_id):
        abort(403)
    form = ArticleForm()
    if form.submit.data and form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        article.section = form.section.data
        project.date_edited = datetime.utcnow()
        article.date_edited = datetime.utcnow()
        article.edited_by = current_user.username
        db.session.commit()
        flash(f"Your article has been updated.")
        return redirect(url_for("articles.article", article_id = article.id, project_id = project.id))
    elif request.method == "GET":
        form.title.data = article.title
        form.content.data = article.content
        form.section.data = article.section
    return render_template("create_article.html", form = form, legend = "Update Article", search_form = search_form)

@articles.route("/project/<int:project_id>/article/<int:article_id>/delete", methods = ["POST"])
@login_required
def delete_article(article_id, project_id):
    project = Project.query.get_or_404(project_id)
    article = Article.query.get_or_404(article_id)
    project.date_edited = datetime.utcnow()
    if article.author != current_user and project.author != current_user and current_user.username not in collab_user(project_id):
        abort(403)
    db.session.delete(article)
    db.session.commit()
    flash(f"Your article has been successfully deleted.")
    return redirect(url_for("projects.project", project_id = project.id))
