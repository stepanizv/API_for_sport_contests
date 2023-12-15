from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateUserForm(FlaskForm):
    first_name = StringField("First Name: ", validators=[DataRequired()])
    last_name = StringField("Last Name: ", validators=[DataRequired()])
    email = StringField("E-mail: ", validators=[DataRequired()])
    sport = StringField("Sport: ", validators=[DataRequired()])
    submit = SubmitField("Submit")

class CreateContestForm(FlaskForm):
    name = StringField("Name: ", validators=[DataRequired()])
    sport = StringField("Sport: ", validators=[DataRequired()])
    submit = SubmitField("Submit")