from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, ValidationError


class MethodForm(FlaskForm):

    method_name = StringField('Method name:', validators=[DataRequired(), Length(2, 30, "Name should be from 2 to 30 symbols.")])

    method_description = StringField('Describe this method:',  validators=[Length(2, 60, "Description couldn't be longer than 60 symbols."), DataRequired("Please enter number of methods.")])

    output_type = SelectField('Type of output:', choices=[('Numeric','Numeric'), ('String','String'), ('Boolean','Boolean')], validators=[DataRequired("Please enter number of methods.")])

    memory_size = SelectField('Memory, reserved for this method:', choices=[('32', '32'), ('64', '64'), ('128', '128'), ('256', '256')], validators=[DataRequired("Please enter memory size.")])

    submit = SubmitField("Save")