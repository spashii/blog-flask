from flask import (Blueprint, render_template, redirect, url_for,
                    flash, abort, request)
from flask_login import current_user, login_required
from blog_flask import db
from blog_flask.models import Post
from blog_flask.posts.forms import PostForm

posts = Blueprint('posts', __name__)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def post_new():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('post_new.html', title='New Post',
                            form=form, legend="Update Post")

@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def post_update(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':        
        form.title.data = post.title
        form.content.data = post.content
    return render_template('post_new.html', title='Update Post',
                            form=form, legend="Update Post")


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def post_delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))
    