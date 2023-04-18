from app import db
from app.main import bp
from flask import render_template


from app.models import User


@bp.route("/")
@bp.route("/index")
def index():

    users_data=[
        {
            "username": "akushyn",
            "email": "akushyn@gmail.com",
            "password": "muny"
        },
        {
            "username": "anton",
            "email": "anton@gmail.com",
            "password": "antonY"
        },
        {
            "username": "denys",
            "email": "denys@gmail.com",
            "password": "danysI"
        },
        {
            "username": "tanya",
            "email": "tanya@gmail.com",
            "password": "tanYa"
        },
        {
            "username": "igor",
            "email": "igor@gmail.com",
            "password": "iGor"
        }
    ]

    for u in users_data:
        user = (
            db.session.query(User)
        .filter(User.username == u.get('username'),
                User.email == u.get('email'),
                User.password == u.get('password')
                ).first()
        )
        if user:
            continue

        user = User(
            username=u.get('username'),
            email=u.get('email'),
            password=u.get('password')
        )
        db.session.add(user)

    db.session.commit()

    users = db.session.query(User).all()



    return render_template("index.html", users=users)

@bp.route('/about')
def about():
    # users = db.session.query(User).all()
    return render_template("about.html")