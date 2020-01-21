from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length, Email, ValidationError


def validStr(form, field):
    for i in field.data:
        if i.lower() not in list('qwertyuioplkjhgfdsazxcvbnm '):
            raise ValidationError('Only letters!!')

class UserForm(FlaskForm):

    user_email = StringField('Users email', validators=[DataRequired(), Length(5, 30), Email("Wrong email format")])

    user_name = StringField('Users name', validators=[DataRequired(),Length(2, 30, "Name should be from 2 to 30 symbols"), validStr])

    user_age = IntegerField('Users age', validators=[DataRequired(), NumberRange(min=12, max=100)])

    user_university = StringField('Users university', validators=[DataRequired(), Length(2)])

    submit = SubmitField("Save")

