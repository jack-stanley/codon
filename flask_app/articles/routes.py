from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flask_app import db
from flask_app.models import Article, Heading, Project
from flask_app.articles.forms import ArticleForm
from datetime import datetime

articles = Blueprint("articles", __name__)

@articles.route("/project/<int:project_id>/article/<int:article_id>")
def article(article_id, project_id):
    project = Project.query.get_or_404(project_id)
    article = Article.query.get_or_404(article_id)
    return render_template("article.html", title = article.title, article = article, project = project)

@articles.route("/project/<int:project_id>/article/new", methods = ["GET", "POST"])
@login_required
def new_article(project_id):
    form = ArticleForm()
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        abort(403)
    if form.validate_on_submit():
        if form.heading.data:
            if form.heading_order.data:
                heading = Heading(heading = form.heading.data, order = form.heading_order.data, overall_project = project)
                article = Article(title = form.title.data, content = form.content.data, header = heading, overall_project = project, author = current_user)
                if Heading.query.filter_by(heading = form.heading.data, project_id = project_id).first() is not None:
                    change = Heading.query.filter_by(heading = form.heading.data, project_id = project_id)
                    for item in change:
                        item.order = form.heading_order.data
            else:
                if Heading.query.filter_by(heading = form.heading.data, project_id = project_id).first() is not None:
                    order = Heading.query.filter_by(heading = form.heading.data, project_id = project_id).first()
                    heading = Heading(heading = form.heading.data, order = order[0].order, overall_project = project)
                    article = Article(title = form.title.data, content = form.content.data, header = heading, overall_project = project, author = current_user)
                else:
                    heading = Heading(heading = form.heading.data, order = 99, overall_project = project)
                    article = Article(title = form.title.data, content = form.content.data, header = heading, overall_project = project, author = current_user)
        else:
            if Heading.query.filter_by(heading = "Other", project_id = project_id).first() is not None:
                order = Heading.query.filter_by(heading = "Other", project_id = project_id).first()
                heading = Heading(heading = "Other", order = order.order, overall_project = project)
                article = Article(title = form.title.data, content = form.content.data, header = heading, overall_project = project, author = current_user)
            else:
                heading = Heading(heading = "Other", order = 100, overall_project = project)
                article = Article(title = form.title.data, content = form.content.data, header = heading, overall_project = project, author = current_user)
        project.date_edited = datetime.utcnow()
        db.session.add(article)
        db.session.commit()
        flash(f"Your article has been created.")
        return redirect(url_for("articles.article", article_id = article.id, project_id = project.id))
    return render_template("create_article.html", form = form, legend = "Create Article")

@articles.route("/project/<int:project_id>/article/<int:article_id>/update", methods = ["GET", "POST"])
@login_required
def update_article(article_id, project_id):
    project = Project.query.get_or_404(project_id)
    article = Article.query.get_or_404(article_id)
    heading = Heading.query.get_or_404(article.header.id)
    if article.author != current_user:
        abort(403)
    form = ArticleForm()
    if form.validate_on_submit():
        article.title = form.title.data
        article.content = form.content.data
        heading.heading = form.heading.data
        heading.order = form.heading_order.data
        project.date_edited = datetime.utcnow()
        article.date_edited = datetime.utcnow()
        change = Heading.query.filter_by(heading = form.heading.data)
        for item in change:
            item.order = form.heading_order.data
        db.session.commit()
        flash(f"Your article has been updated.")
        return redirect(url_for("articles.article", article_id = article.id, project_id = project.id))
    elif request.method == "GET":
        form.title.data = article.title
        form.content.data = article.content
        form.heading.data = heading.heading
        form.heading_order.data = heading.order
    return render_template("create_article.html", form = form, legend = "Update Article")

@articles.route("/project/<int:project_id>/article/<int:article_id>/delete", methods = ["POST"])
@login_required
def delete_article(article_id, project_id):
    project = Project.query.get_or_404(project_id)
    article = Article.query.get_or_404(article_id)
    heading = Heading.query.get_or_404(article.header.id)
    if article.author != current_user:
        abort(403)
    db.session.delete(article)
    db.session.delete(heading)
    db.session.commit()
    flash(f"Your article has been successfully deleted.")
    return redirect(url_for("projects.project", project_id = project.id))
