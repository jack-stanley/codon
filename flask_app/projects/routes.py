from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flask_app import db
from flask_app.models import Project, Article, Tag, User, Tube
from flask_app.projects.forms import ProjectForm
from flask_app.main.forms import SearchForm
from flask_app.projects.utils import save_banner
from datetime import datetime

projects = Blueprint("projects", __name__)

@projects.route("/project/new", methods = ["GET", "POST"])
@login_required
def new_project():
    search_form = SearchForm()
    if search_form.submit_search.data and search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    form = ProjectForm()
    if form.submit.data and form.validate_on_submit():
        stripped = form.tags.data.strip()
        split_tags_list = stripped.split(", ")
        if form.banner_image.data:
            project = Project(project_title = form.project_title.data, date_edited = datetime.utcnow(), banner_image = save_banner(form.banner_image.data), abstract = form.abstract.data, author = current_user, collaborators = form.collaborators.data.strip())
            for item in split_tags_list:
                tag = Tag(tag = item, overall_project = project)
            db.session.add(tag)
            db.session.add(project)
            db.session.commit()
        else:
            project = Project(project_title = form.project_title.data, date_edited = datetime.utcnow(), abstract = form.abstract.data, author = current_user, collaborators = form.collaborators.data.strip())
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
    if search_form.submit_search.data and search_form.validate_on_submit():
        search_query = search_form.search_query.data
        return redirect(url_for("main.search", search_query = search_query, search_type = "project_search"))
    project = Project.query.get_or_404(project_id)
    articles_intro = Article.query.filter_by(overall_project = project, section = "Introduction").order_by(Article.date_edited.desc()).all()
    articles_main = Article.query.filter_by(overall_project = project, section = "Main").order_by(Article.date_edited.desc()).all()
    articles_resources = Article.query.filter_by(overall_project = project, section = "Resources").order_by(Article.date_edited.desc()).all()
    articles_misc = Article.query.filter_by(overall_project = project, section = "miscellaneous").order_by(Article.date_edited.desc()).all()
    tags = Tag.query.filter_by(overall_project = project)

    collabs = project.collaborators
    stripped = collabs.strip()
    split_tags_list = stripped.split(", ")
    c = []
    for item in split_tags_list:
        c.append(item)

    if current_user.is_authenticated:
        user_id = current_user.id
    else:
        user_id = "not_authenticated"
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

    project_pic = url_for("static", filename = "images/project_pics/" + project.banner_image)
    profile_pic = url_for("static", filename = "images/profile_pics/" + project.author.image_file)
    return render_template("project.html", tube_count = tube_count, toggle_colour = toggle_colour, user_id = user_id, articles_intro = articles_intro, articles_main = articles_main, articles_resources = articles_resources, articles_misc = articles_misc, collabs = c, search_form = search_form, title = project.project_title, project = project, project_tags = tags, project_pic = project_pic, profile_pic = profile_pic)

@projects.route("/project/<int:project_id>/update", methods = ["GET", "POST"])
@login_required
def update_project(project_id):
    search_form = SearchForm()
    if search_form.submit_search.data and search_form.validate_on_submit():
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
    if form.submit.data and form.validate_on_submit():

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
        project.collaborators = form.collaborators.data
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
        form.collaborators.data = project.collaborators
    return render_template("create_project.html", form = form, legend = "Update Project", search_form = search_form)

@projects.route("/project/<int:project_id>/delete", methods = ["POST"])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    articles = Article.query.filter_by(overall_project = project)
    tags = Tag.query.filter_by(overall_project = project)
    tubes = Tube.query.filter_by(overall_project = project)
    if project.author != current_user:
        abort(403)
    for article in articles:
        db.session.delete(article)
    for tag in tags:
        db.session.delete(tag)
    for tube in tubes:
        db.session.delete(tube)
    db.session.delete(project)
    db.session.commit()
    flash(f"Your project has been successfully deleted.")
    return redirect(url_for("main.browse"))
