from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError


class HastagForm(FlaskForm):

    words = StringField('Enter description:', validators=[DataRequired("Please enter something to search."), Length(3)])

    choice = SelectField('choose object', choices=[('class', 'class'), ('method', 'method'), ('parameter', 'parameter')],
                      validators=[DataRequired("Please enter object.")])

    submit = SubmitField("Search")