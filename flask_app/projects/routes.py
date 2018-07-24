from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flask_app import db
from flask_app.models import Project, Article, Heading
from flask_app.projects.forms import ProjectForm
from flask_app.projects.utils import save_banner
from datetime import datetime

projects = Blueprint("projects", __name__)

@projects.route("/project/new", methods = ["GET", "POST"])
@login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():
        if form.banner_image.data:
            project = Project(project_title = form.project_title.data, banner_image = save_banner(form.banner_image.data), abstract = form.abstract.data, author = current_user, tags = form.tags.data)
            db.session.add(project)
            db.session.commit()
        else:
            project = Project(project_title = form.project_title.data, abstract = form.abstract.data, author = current_user, tags = form.tags.data)
            db.session.add(project)
            db.session.commit()
        flash(f"Your project has been created.")
        return redirect(url_for("main.browse"))
    return render_template("create_project.html", form = form, legend = "Create Project")

@projects.route("/project/<int:project_id>")
def project(project_id):
    project = Project.query.get_or_404(project_id)
    articles = Article.query.filter_by(overall_project = project).order_by(Article.date_posted.desc())
    headings = Heading.query.filter_by(overall_project = project).order_by(Heading.order.asc())

    l = []
    for heading in headings:
        l.append(heading.heading)
    unique = []
    for item in l:
        if item not in unique:
            unique.append(item)

    project_pic = url_for("static", filename = "images/project_pics/" + project.banner_image)
    profile_pic = url_for("static", filename = "images/profile_pics/" + project.author.image_file)
    return render_template("project.html", title = project.project_title, project = project, articles = articles, headings_title = unique, headings = headings, project_pic = project_pic, profile_pic = profile_pic)

@projects.route("/project/<int:project_id>/update", methods = ["GET", "POST"])
@login_required
def update_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        abort(403)
    form = ProjectForm()
    if form.validate_on_submit():
        project.project_title = form.project_title.data
        project.abstract = form.abstract.data
        project.tags = form.tags.data
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
        form.tags.data = project.tags
    return render_template("create_project.html", form = form, legend = "Update Project")

@projects.route("/project/<int:project_id>/delete", methods = ["POST"])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.author != current_user:
        abort(403)
    db.session.delete(project)
    db.session.commit()
    flash(f"Your project has been successfully deleted.")
    return redirect(url_for("main.browse", project_id = project.id))
