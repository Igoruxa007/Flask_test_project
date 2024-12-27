from __future__ import annotations

from typing import Any

from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import Field
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo
from wtforms.validators import Length
from wtforms.validators import ValidationError

from webapp.user.models import User


class LoginForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
    )
    remember_me = BooleanField(
        'Запомнить меня',
        default=True,
        render_kw={'class': 'form-check-input'},
    )
    submit = SubmitField(
        'Отправить',
        render_kw={'class': 'btn btn-primary'},
    )


class RegistrationForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
    )
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()],
        render_kw={'class': 'form-control'},
    )
    password = PasswordField(
        'Пароль',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
    )
    password2 = PasswordField(
        'Повторите пароль',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={'class': 'form-control'},
    )
    submit = SubmitField('Отправить', render_kw={'class': 'btn btn-primary'})

    def validate_username(self, username: Field) -> None:
        user_count = User.query.filter_by(username=username.data).count()
        if user_count > 0:
            raise ValidationError('Пользователь с таким именем уже существует')

    def validate_email(self, email: Field) -> None:
        user_count = User.query.filter_by(email=email.data).count()
        if user_count > 0:
            raise ValidationError(
                'Пользователь с такой электронной почтой уже зарегестрирован',
            )


class EditProfForm(FlaskForm):
    username = StringField(
        'Имя пользователя',
        validators=[DataRequired()],
        render_kw={'class': 'form-control'},
    )
    about_me = TextAreaField(
        'Обо мне',
        validators=[Length(min=0, max=140)],
        render_kw={'class': 'form-control'},
    )
    submit = SubmitField('Submit')

    def __init__(self, original_uesrname: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.original_username = original_uesrname

    def validate_username(self, username: Field) -> None:
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class PostForm(FlaskForm):
    post = TextAreaField(
        'Write poem:', validators=[
            DataRequired(), Length(min=1, max=300),
        ],
    )
    submit = SubmitField('Запостить')
