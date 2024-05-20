from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from webapp.user.models import User


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    password = PasswordField('Пароль',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    remember_me = BooleanField('Запомнить меня',
                               default=True,
                               render_kw={"class": "form-check-input"})
    submit = SubmitField('Отправить',
                         render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    email = StringField('Email',
                        validators=[DataRequired(), Email()],
                        render_kw={"class": "form-control"})
    password = PasswordField('Пароль',
                             validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль',
                              validators=[DataRequired(), EqualTo('password')],
                              render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        user_count = User.query.filter_by(username=username.data).count()
        if user_count > 0:
            raise ValidationError('Пользователь с таким именем уже существует')

    def validate_email(self, email):
        user_count = User.query.filter_by(email=email.data).count()
        if user_count > 0:
            raise ValidationError(
                'Пользователь с такой электронной почтой уже зарегестрирован'
            )


class EditProfForm(FlaskForm):
    username = StringField('Имя пользователя',
                           validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    about_me = TextAreaField('Обо мне',
                             validators=[Length(min=0, max=140)],
                             render_kw={"class": "form-control"})
    submit = SubmitField('Submit')
