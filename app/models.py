from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


class User(db.Model, UserMixin):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    animals: so.WriteOnlyMapped["Pokedex"] = so.relationship(back_populates="owner")

    def __repr__(self):
        return f"<User{self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Pokedex(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    user_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(512))
    owner: so.Relationship[User] = so.relationship(back_populates="animals")
    attributes: so.WriteOnlyMapped["Attributes"] = so.relationship(
        back_populates="animal"
    )

    def __repr__(self):
        return f"{self.name}"


class Attributes(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    animal_id: so.Mapped[str] = so.mapped_column(sa.ForeignKey(Pokedex.id), index=True)
    animal: so.Relationship[Pokedex] = so.relationship(back_populates="attributes")
    trainability: so.Mapped[int] = so.mapped_column(sa.Integer)
    intelligence: so.Mapped[int] = so.mapped_column(sa.Integer)
    protection: so.Mapped[int] = so.mapped_column(sa.Integer)
    playfulness: so.Mapped[int] = so.mapped_column(sa.Integer)
    energy: so.Mapped[int] = so.mapped_column(sa.Integer)


class Dogs(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    breed: so.Mapped[int] = so.mapped_column(sa.String(64))
