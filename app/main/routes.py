from flask import render_template, flash, redirect, url_for
from app import db

from app.main import bp


@bp.route("/")
@bp.route("/index")
def index():
    return render_template("index.html")
