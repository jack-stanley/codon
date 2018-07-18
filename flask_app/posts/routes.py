from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flask_app import db
from flask_app.models import Post
from flask_app.posts.forms import PostForm

posts = Blueprint("posts", __name__)

@posts.route("/post/new", methods = ["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user, tags = form.tags.data)
        db.session.add(post)
        db.session.commit()
        flash(f"Your post has been created.")
        return redirect(url_for("main.browse"))
    return render_template("create_post.html", form = form, legend = "Create Post")

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title = post.title, post = post)

@posts.route("/post/<int:post_id>/update", methods = ["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f"Your post has been updated.")
        return redirect(url_for("posts.post", post_id = post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", form = form, legend = "Update Post")

@posts.route("/post/<int:post_id>/delete", methods = ["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f"Your post has been successfully deleted.")
    return redirect(url_for("main.browse"))
