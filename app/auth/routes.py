from app.auth import bp
from flask import render_template, redirect, url_for, flash
from .forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user
from .. import db
from ..models import User, Profile


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("Invalid username/password", category='error')
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember.data)

        return redirect(url_for("main.view_profile", user_id=current_user.id))
    return render_template("auth/login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password((form.password.data))

        db.session.add(user)
        db.session.commit()
        profile = Profile(
                          user_id=user.id,
                          first_name=form.first_name.data,
                          last_name=form.last_name.data,
                          Linkedln_URL=form.Linkedln_profile.data,
                          Facebook_URL=form.Facebook_profile.data
                         )
        db.session.add(profile)
        db.session.commit()
        flash("Successfuly registered", category='success')

        login_user(user)

        return redirect(url_for("main.view_profile", user_id=current_user.id))
    return render_template("auth/register.html", form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
