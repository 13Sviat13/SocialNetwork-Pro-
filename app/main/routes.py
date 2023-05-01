from app import db
from app.main import bp

from flask_login import current_user, login_required
from flask import render_template
from app.models import User, Profile


@bp.route("/")
@bp.route("/index")
def index():

    users_data = []
    profile_data = []
    for u in users_data:
        user = (
            db.session.query(User)
            .filter(
                User.username == u.get('username'),
                User.email == u.get('email'),
            ).first()
        )
        if user:
            continue

        user = User(
            username=u.get('username'),
            email=u.get('email'),
        )
        db.session.add(user)

    for p in profile_data:
        profile = (
            db.session.query(Profile)
            .filter(
                Profile.first_name == p.get('first_name'),
                Profile.last_name == p.get('last_name'),
                Profile.Linkedln_URL == p.get('Linkedln_profile'),
                Profile.Facebook_URL == p.get('Facebook_profile')
                ).first()
               )
        if profile:
            continue

        profile = Profile(
            first_name=p.get('first_name'),
            last_name=p.get('last_name'),
            Linkedln_URL=p.get('Linkedln_profile'),
            Facebook_URL=p.get('Facebook_profile')
        )
        db.session.add(profile)

    db.session.commit()

    users = db.session.query(User).all()
    profiles = db.session.query(Profile).all()

    return render_template("index.html", users=users, profiles=profiles)


@bp.route('/about')
def about():
    # users = db.session.query(User).all()
    return render_template("about.html")


@bp.route('/profile/<int:user_id>')
@login_required
def view_profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    profile = Profile.query.filter_by(user_id=user_id).first()
    return render_template('profile.html', user=user, profile=profile, current_user=current_user)
