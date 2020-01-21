from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError


class NeuronForm(FlaskForm):

    output_type = SelectField('Type of output:', choices=[('Numeric', 'Numeric'), ('String', 'String'), ('Boolean', 'Boolean')], validators=[DataRequired("Please enter number of methods.")])

    memory_size = SelectField('Memory, reserved for this method:', choices=[('32', '32'), ('64', '64'), ('128', '128'), ('256', '256')], validators=[DataRequired("Please enter memory size.")])

    submit = SubmitField("Save")