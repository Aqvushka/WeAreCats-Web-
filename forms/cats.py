from lib2to3.fixer_util import String

from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, BooleanField, StringField, IntegerField, SelectField
from wtforms.validators import DataRequired


class CatForm(FlaskForm):
    name = StringField('Имя котика', validators=[DataRequired()])
    age = IntegerField('Возраст котика', validators=[DataRequired()])
    breed = SelectField('Порода', choices=[
        ('', 'Выберите породу'),
        ('unknown', 'Неизвестно'),
        ('british', 'Британская'),
        ('persian', 'Персидская'),
        ('maine_coon', 'Мейн-кун'),
        ('ragdoll', 'Рэгдолл'),
        ('sphynx', 'Сфинкс'),
        ('scottish_fold', 'Шотландская вислоухая'),
        ('siamese', 'Сиамская'),
        ('abyssinian', 'Абиссинская'),
        ('bengal', 'Бенгальская'),
        ('russian_blue', 'Русская голубая'),
        ('birman', 'Бирманская'),
        ('norwegian_forest', 'Норвежская лесная'),
        ('american_shorthair', 'Американская короткошерстная'),
        ('oriental', 'Ориентальная'),
        ('devon_rex', 'Девон-рекс'),
        ('exotic', 'Экзотическая короткошерстная'),
        ('burmese', 'Бурманская'),
        ('himalayan', 'Гималайская'),
        ('cornish_rex', 'Корниш-рекс')], validators=[DataRequired()])
    features = StringField('Особенности котика', validators=[DataRequired()])
    submit = SubmitField('Добавить котика')
