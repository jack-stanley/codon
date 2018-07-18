from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flask_app import db
from flask_app.models import Project
from flask_app.projects.forms import ProjectForm

projects = Blueprint("projects", __name__)
