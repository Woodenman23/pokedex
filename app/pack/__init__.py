from flask import Blueprint

bp = Blueprint("pack", __name__)

from app.pack import routes  # noqa: E402, F401
