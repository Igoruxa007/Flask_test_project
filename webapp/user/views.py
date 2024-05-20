from flask_login import current_user, login_user, logout_user, login_required
from flask import Blueprint, render_template, flash, redirect, url_for, request

from webapp.model import db
from webapp.user.forms import LoginForm, RegistrationForm, EditProfForm
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно вышли из учетной записи')
    return redirect(url_for('news.index'))


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template('users/login.html',
                           page_title=title,
                           form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            return redirect(url_for('news.index'))
    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    form = RegistrationForm()
    title = 'Регистрация'
    return render_template('users/registration.html',
                           page_title=title,
                           form=form)


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}":- {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
        return redirect(url_for('user.register'))


@blueprint.route('/<username>')
def user_page(username):
    if not current_user.is_authenticated:
        return redirect(url_for('news.index'))
    user = User.query.filter_by(username=username).first_or_404()
    title = 'Ваши данные'
    return render_template('users/user_page.html',
                           page_title=title,
                           user_data=user)


@blueprint.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile():
    form = EditProfForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Изменения внсены')
        return redirect(url_for('user.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('users/edit_profile.html',
                           title='Edit profile',
                           form=form)
