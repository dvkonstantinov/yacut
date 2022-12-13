from flask_wtf import FlaskForm
from wtforms import URLField, StringField
from wtforms.validators import DataRequired, Length, Optional, Regexp


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        id='form-title',
        render_kw={
            'class': 'form-control form-control-lg py-2 mb-3',
            'placeholder': 'Длинная ссылка'
        },
        validators=[DataRequired(message='Обязательное поле')]
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        id='form-link',
        render_kw={
            'class': 'form-control form-control-lg py-2 mb-3',
            'placeholder': 'Ваш вариант короткой ссылки'
        },
        validators=[Length(1, 16, message='Нужно от 1 до 16 символов'),
                    Optional(),
                    Regexp(regex='^[a-zA-Z0-9]*$',
                           message='Поле может содержать только буквы и '
                                   'цифры')]
    )
