from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired


class AnimalForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description")
    image = FileField(
        "Photo",
        validators=[FileAllowed(["jpg", "png", "jpeg"])],
    )
    submit = SubmitField("Join the Pack")
