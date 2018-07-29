from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flask_app import db
from flask_app.models import Project, Article, Heading, Tag
from flask_app.projects.forms import ProjectForm
from flask_app.main.forms import SearchForm
from flask_app.projects.utils import save_banner
from datetime import datetime

projects = Blueprint("projects", __name__)

@projects.route("/project/new", methods = ["GET", "POST"])
@login_required
def new_project():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    form = ProjectForm()
    if form.validate_on_submit():
        stripped = form.tags.data.strip()
        split_tags_list = stripped.split(", ")
        if form.banner_image.data:
            project = Project(project_title = form.project_title.data, banner_image = save_banner(form.banner_image.data), abstract = form.abstract.data, author = current_user)
            for item in split_tags_list:
                tag = Tag(tag = item, overall_project = project)
            db.session.add(tag)
            db.session.add(project)
            db.session.commit()
        else:
            project = Project(project_title = form.project_title.data, abstract = form.abstract.data, author = current_user)
            for item in split_tags_list:
                tag = Tag(tag = item, overall_project = project)
            db.session.add(tag)
            db.session.add(project)
            db.session.commit()
        flash(f"Your project has been created.")
        return redirect(url_for("projects.project", project_id = project.id))
    return render_template("create_project.html", form = form, legend = "Create Project", search_form = search_form)

@projects.route("/project/<int:project_id>", methods = ["GET", "POST"])
def project(project_id):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    project = Project.query.get_or_404(project_id)
    articles = Article.query.filter_by(overall_project = project).order_by(Article.date_posted.desc())
    headings = Heading.query.filter_by(overall_project = project).order_by(Heading.order.asc())
    tags = Tag.query.filter_by(overall_project = project)
    tags_len = Tag.query.filter_by(overall_project = project).count

    t = ""
    for item in tags:
        if item == tags[0]:
            t = t + item.tag
        elif tags_len != 1:
            t = t + ", " + item.tag

    h = []
    for heading in headings:
        h.append(heading.heading)
    unique = []
    for item in h:
        if item not in unique:
            unique.append(item)

    project_pic = url_for("static", filename = "images/project_pics/" + project.banner_image)
    profile_pic = url_for("static", filename = "images/profile_pics/" + project.author.image_file)
    return render_template("project.html", search_form = search_form, title = project.project_title, project = project, articles = articles, headings_title = unique, headings = headings, project_tags = t, project_pic = project_pic, profile_pic = profile_pic)

@projects.route("/project/<int:project_id>/update", methods = ["GET", "POST"])
@login_required
def update_project(project_id):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    project = Project.query.get_or_404(project_id)
    tags = Tag.query.filter_by(overall_project = project)
    tags_len = Tag.query.filter_by(overall_project = project).count

    t = ""
    for item in tags:
        if item == tags[0]:
            t = t + item.tag
        elif tags_len != 1:
            t = t + ", " + item.tag

    if project.author != current_user:
        abort(403)
    form = ProjectForm()
    if form.validate_on_submit():

        stripped = form.tags.data.strip()
        split_tags_list = stripped.split(", ")
        for tag in tags:
            db.session.delete(tag)
        for item in split_tags_list:
            tag = Tag(tag = item, overall_project = project)
        db.session.add(tag)

        project.project_title = form.project_title.data
        project.abstract = form.abstract.data
        project.date_edited = datetime.utcnow()
        if form.banner_image.data:
            picture_file = save_banner(form.banner_image.data)
            project.banner_image = picture_file
        db.session.commit()
        flash(f"Your project has been updated.")
        return redirect(url_for("projects.project", project_id = project.id))
    elif request.method == "GET":
        form.project_title.data = project.project_title
        form.abstract.data = project.abstract
        form.tags.data = t
    return render_template("create_project.html", search_form = search_form, form = form, legend = "Update Project")

@projects.route("/project/<int:project_id>/delete", methods = ["POST"])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    articles = Article.query.filter_by(overall_project = project)
    headings = Heading.query.filter_by(overall_project = project)
    tags = Tag.query.filter_by(overall_project = project)
    if project.author != current_user:
        abort(403)
    for article in articles:
        db.session.delete(article)
    for heading in headings:
        db.session.delete(heading)
    for tag in tags:
        db.session.delete(tag)
    db.session.delete(project)
    db.session.commit()
    flash(f"Your project has been successfully deleted.")
    return redirect(url_for("main.browse"))
