from app import db
from ..models import User, Post, Follow
from app.post.forms import PostForm
from app.user import bp
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from app.user.forms import ProfileForm


@bp.route("/blog")
def blog():
    form = PostForm()
    posts = (
        db.session.query(Post)
        .filter(
            Post.author_id == current_user.id
               )
        .order_by(Post.created_at.desc())
        .all()
            )
    return render_template("user/blog.html", posts=posts, form=form)


@bp.route("profile/<string:username>", methods=['GET', 'POST'])
@login_required
def user(username):
    user = db.session.query(User).filter(User.username == username).first_or_404()
    return render_template('user/profile.html', user=user, username=user.username)


@bp.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.profile.first_name = form.first_name.data
        current_user.profile.last_name = form.last_name.data
        current_user.profile.facebook = form.facebook.data
        current_user.profile.linkedin = form.linkedin.data
        current_user.profile.bio = form.bio.data
        db.session.commit()
        flash("Your changes have been saved", category="success")
        return redirect(url_for('user.edit_profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.profile.first_name
        form.last_name.data = current_user.profile.last_name
        form.first_name.data = current_user.profile.first_name
        form.facebook.data = current_user.profile.facebook
        form.linkedin.data = current_user.profile.linkedin
        form.bio.data = current_user.profile.bio
    return render_template('user/edit_profile.html', title='Edit Profile', form=form)


@bp.route('/user/<username>/follow', methods=['POST'])
@login_required
def follow_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if current_user.is_to_subscribed(user):
        flash(f'You have already following {username}', category='warning')
    else:
        subscription = Follow(follower_id=current_user.id, followee_id=user.id)
        db.session.add(subscription)
        db.session.commit()
        flash(f'You are now following {username}.', 'success')
    return redirect(url_for('user.user', username=user.username))


@bp.route('/user/<username>/unfollow', methods=['POST'])
@login_required
def unfollow_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user != current_user:
        subscription = Follow.query.filter_by(follower_id=current_user.id, followee_id=user.id).first()
        if subscription:
            db.session.delete(subscription)
            db.session.commit()
            flash(f'You have unfollowed {username}.', 'success')
        else:
            flash(f"You are not following {username}.", 'warning')
    else:
        flash('You cannot unfollow yourself.', 'danger')
    return redirect(url_for('user.user', username=user.username))


def follow_list(username):
    user = User.query.filter_by(username=username).first_or_404()
    followers = user.followers.all()
    following = user.following.all()
    return redirect(url_for('user.user', username=user.username, followers=followers, following=following))
