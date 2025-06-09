from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, BooleanField, StringField, IntegerField
from wtforms.validators import DataRequired


class ShelterForm(FlaskForm):
    name = StringField('Название приюта', validators=[DataRequired()])
    phone = StringField('Контактный номер', validators=[DataRequired()])
    address = StringField('Адрес', validators=[DataRequired()])
    submit = SubmitField('Добавить приют')
