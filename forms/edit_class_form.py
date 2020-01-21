from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError


class EditClassForm(FlaskForm):

    methods_quantity = IntegerField('Number of methods',  validators=[DataRequired("Please enter number of methods."), NumberRange(min=1, max=4)])

    class_description = StringField('Describe this class:', validators=[ DataRequired(), Length(2, 60, "Description couldn't be longer than 60 symbols.")])

    submit = SubmitField("Save")