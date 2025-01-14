from app import db
import sqlalchemy as sa
from flask import render_template, flash, redirect, url_for
from app.models import Pokedex
from app.pack import bp
from flask_login import current_user
from app.pack.forms import AnimalForm


@bp.route("/")
@bp.route("/index")
def index():
    if current_user.is_authenticated:
        redirect(url_for("main.index"))
    pack = db.session.scalars(sa.select(Pokedex).where(Pokedex.owner == current_user))

    return render_template("pack/index.html", pack=pack)


@bp.route("/create", methods=["GET", "POST"])
def create():
    if current_user.is_authenticated:
        redirect(url_for("main.index"))
    form = AnimalForm()
    if form.validate_on_submit():
        dog = Pokedex(
            name=form.name.data,
            user_id=current_user.id,
            description=form.description.data,
        )
        db.session.add(dog)
        db.session.commit()
        return redirect(url_for("pack.get", dog_id=dog.id))
    return render_template("pack/create.html", form=form)


temp_attributes = {
    "id": 1,
    "animal": "Big Dog",
    "trainability": 10,
    "intelligence": 10,
    "protection": 10,
    "playfulness": 10,
    "energy": 10,
}


@bp.route("/<int:dog_id>")
def get(dog_id):
    dog = db.session.scalar(sa.select(Pokedex).where(Pokedex.id == dog_id))
    if dog and dog.owner == current_user:
        print(dog)
        return render_template("pack/dog.html", data=dog, attributes=temp_attributes)
    return "<h1> There is nothing here"


@bp.route("/<int:dog_id>/update")
def update(dog_id):
    dog = db.session.scalar(sa.select(Pokedex).where(Pokedex.id == dog_id))
    if not dog and not dog.owner == current_user:
        return redirect(url_for("pack.get", dog_id=dog_id))
    return "<h1> Unknown dogs <h1>"


@bp.route("/<int:dog_id>/delete")
def delete(dog_id):
    dog = db.session.scalar(sa.select(Pokedex).where(Pokedex.id == dog_id))
    if dog and dog.owner == current_user:
        return redirect(url_for("pack.index"))
    return "<h1> There is nothing here"
