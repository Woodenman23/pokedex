from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user
import sqlalchemy as sa
import torch
import torchvision.models as models

from PIL import Image

from app import db, PROJECT_ROOT, MODEL_PATH
from app.models import Pokedex
from . import pack_bp, dog_breeds, num_dog_breeds, transform
from app.pack.forms import AnimalForm
from .wiki import wiki_summary


@pack_bp.route("/")
@pack_bp.route("/index")
def index():
    if current_user.is_authenticated:
        redirect(url_for("main.index"))
    pack = db.session.scalars(sa.select(Pokedex).where(Pokedex.owner == current_user))

    return render_template("pack/index.html", pack=pack)


@pack_bp.route("/create", methods=["GET", "POST"])
def create():
    if current_user.is_authenticated:
        redirect(url_for("main.index"))

    form = AnimalForm()
    if form.validate_on_submit():
        image_file = PROJECT_ROOT / f"app/static/uploads/images/{form.name.data}.jpeg"
        image = form.image.data
        image.save(image_file)
        image = Image.open(str(image_file))

        # run image through identifier
        model = models.convnext_large(pretrained=True)
        model.classifier[-1] = torch.nn.Linear(
            model.classifier[-1].in_features, num_dog_breeds
        )
        model.load_state_dict(
            torch.load(str(MODEL_PATH), map_location=torch.device("cpu"))
        )

        input_tensor = transform(image).unsqueeze(0)

        model.eval()
        with torch.no_grad():
            output = model(input_tensor)

        probabilities = torch.nn.functional.softmax(output, dim=1)
        top3_probs, top3_indices = torch.topk(probabilities, 3)

        results = ""
        for i in range(3):
            results += f"{dog_breeds[top3_indices[0][i].item()][10:]}, Probability: {str(top3_probs[0][i].item() * 100)[:5]}%\n"

        description = wiki_summary(dog_breeds[top3_indices[0][0].item()][10:])
        # if not found ask chatgpt for a summary

        db.add(Pokedex())

        return render_template(
            "dog.html",
            dog_image=url_for(
                "static", filename=f"uploads/images/{form.name.data}.jpeg"
            ),
            results=results,
        )

        # if not, offer alternative breeds
        # assign attributes
        # add to db

        # dog = Pokedex(
        #     name=form.name.data,
        #     user_id=current_user.id,
        #     image=form.image.data,
        # )
        # db.session.add(dog)
        # db.session.commit()
        # return redirect(url_for("pack.get", dog_id=dog.id))

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


@pack_bp.route("/<int:dog_id>")
def get(dog_id):
    dog = db.session.scalar(sa.select(Pokedex).where(Pokedex.id == dog_id))
    if dog and dog.owner == current_user:
        print(dog)
        return render_template("pack/dog.html", data=dog, attributes=temp_attributes)
    return "<h1> There is nothing here"


@pack_bp.route("/<int:dog_id>/update")
def update(dog_id):
    dog = db.session.scalar(sa.select(Pokedex).where(Pokedex.id == dog_id))
    if not dog and not dog.owner == current_user:
        return redirect(url_for("pack.get", dog_id=dog_id))
    return "<h1> Unknown dogs <h1>"


@pack_bp.route("/<int:dog_id>/delete")
def delete(dog_id):
    dog = db.session.scalar(sa.select(Pokedex).where(Pokedex.id == dog_id))
    if dog and dog.owner == current_user:
        return redirect(url_for("pack.index"))
    return "<h1> There is nothing here"
