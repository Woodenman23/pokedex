from flask import render_template, flash, redirect, url_for
from app.auth.forms import LoginForm, RegisterForm
from app import db
import sqlalchemy as sa
from app.models import User
from flask_login import login_user, current_user, logout_user
from app.auth import bp


@bp.route("/login", methods=["GET", "POST"])
def login():
    print(current_user.is_authenticated)
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("main.index"))
    return render_template("auth/login.html", title="Sign In", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("pack.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", title="Register", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))
