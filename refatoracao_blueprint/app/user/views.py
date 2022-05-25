from flask import redirect, render_template, url_for
from flask_login import login_required

from app import db
from app.models import User

from . import user


@user.route("/")
def index():
    users = User.query.all() # Select * from users; 
    return render_template("users.html", users=users)

@user.route("/user/<int:id>")
@login_required
def unique(id):
    user = User.query.get(id)
    return render_template("user.html", user=user)

@user.route("/user/delete/<int:id>")
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for(".index"))
