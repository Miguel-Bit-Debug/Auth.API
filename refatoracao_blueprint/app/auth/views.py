from datetime import timedelta

from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.forms import LoginForm, RegisterForm
from app.models import User

from . import auth


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User()
        user.name = form.name.data
        user.email = form.email.data
        user.password = generate_password_hash(form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("register.html", form=form)

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if not user:
            flash("Credênciais incorretas", "danger")
            return redirect(url_for(".login"))

        if not check_password_hash(user.password, form.password.data):
            flash("Credênciais incorretas", "danger")
            return redirect(url_for(".login"))

        login_user(user, remember=form.remember.data, duration=timedelta(days=7))
        return redirect(url_for("index"))

    return render_template("login.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))
