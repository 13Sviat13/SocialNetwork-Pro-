from app import db
from ..models import Post, Like, Dislike
from app.post import bp
from .forms import PostForm
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_required


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()

    if request.method == "POST":
        if form.validate_on_submit():
            post = Post(title=form.title.data, content=form.content.data, author=current_user)

            db.session.add(post)
            db.session.commit()
            flash('Your post has been creates!', 'success')
        else:
            title = form.title.data

            if not title or len(title) < 2:
                flash('Title must be at least 3 characters long', category="error")

        return redirect(url_for("user.blog"))
    return render_template('user/blog.html', title='Create Post', form=form)


@bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post has been updated!", category="success")
        return redirect(url_for("user.blog"))
    elif request.method == 'GET':
        if current_user.id == post.author_id:
            form.title.data = post.title
            form.content.data == post.content
    return render_template('user/blog.html', title='Edit Post', form=form, post=post)


@bp.route('/<int:post_id>/like', methods=['GET', 'POST'])
@login_required
def like(post_id):
    post = Post.query.get_or_404(post_id)
    liked = Like.query.filter_by(user=current_user, post=post).first()
    disliked = Dislike.query.filter_by(user=current_user, post=post).first()

    if disliked:
        db.session.delete(disliked)
        db.session.commit()
        like_post = Like(user=current_user, post=post)
        db.session.add(like_post)
        db.session.commit()
        flash('You have liked this post!', 'success')
    elif liked:
        db.session.delete(liked)
        db.session.commit()
        flash('You have  uliked this post!', 'warning')
    else:
        like_post = Like(user=current_user, post=post)
        db.session.add(like_post)
        db.session.commit()
        flash('You have liked this post!', 'success')
    return redirect(request.referrer)


@bp.route('/<int:post_id>/dislike', methods=['GET', 'POST'])
@login_required
def dislike(post_id):
    post = Post.query.get_or_404(post_id)
    liked = Like.query.filter_by(user=current_user, post=post).first()
    disliked = Dislike.query.filter_by(user=current_user, post=post).first()

    if disliked:
        db.session.delete(disliked)
        db.session.commit()
        flash('You have  udisliked this post!', 'warning')
    elif liked:
        db.session.delete(liked)
        db.session.commit()
        dislike_post = Dislike(user=current_user, post=post)
        db.session.add(dislike_post)
        db.session.commit()
        flash('You have disliked this post!', 'success')
    else:
        dislike_post = Dislike(user=current_user, post=post)
        db.session.add(dislike_post)
        db.session.commit()
        flash('You have disliked this post!', 'success')
    return redirect(request.referrer)


@bp.route('/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('user.blog'))
