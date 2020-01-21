from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError


class EditParameterForm(FlaskForm):

    parameter_type = StringField('Parameter type:', validators=[DataRequired("Please enter parameter type."),Length(2, 30, "Type couldn't be longer than 30 symbols")])

    parameter_description = StringField('Please enter a description.', validators=[DataRequired(), Length(2, 60, "Description couldn't be longer than 60 symbols")])

    submit = SubmitField("Save")