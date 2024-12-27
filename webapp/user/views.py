from __future__ import annotations

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug import Response

from webapp.model import db
from webapp.user.forms import EditProfForm
from webapp.user.forms import LoginForm
from webapp.user.forms import PostForm
from webapp.user.forms import RegistrationForm
from webapp.user.models import Post
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/user')


@blueprint.route('/logout')
def logout() -> Response:
    logout_user()
    flash('Вы успешно вышли из учетной записи')
    return redirect(url_for('news.index'))


@blueprint.route('/login')
def login() -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = 'Авторизация'
    login_form = LoginForm()
    return render_template(
        'users/login.html',
        page_title=title,
        form=login_form,
    )


@blueprint.route('/process-login', methods=['POST'])
def process_login() -> Response:
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
def register() -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    form = RegistrationForm()
    title = 'Регистрация'
    return render_template(
        'users/registration.html',
        page_title=title,
        form=form,
    )


@blueprint.route('/process-reg', methods=['POST'])
def process_reg() -> Response:
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            role='user',
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(
                    'Ошибка в поле "{}":- {}'.format(
                        getattr(form, field).label.text,
                        error,
                    ),
                )
        return redirect(url_for('user.register'))


@blueprint.route('/<username>')
def user_page(username: str) -> Response | str:
    if not current_user.is_authenticated:
        return redirect(url_for('news.index'))
    user = User.query.filter_by(username=username).first_or_404()
    title = 'Ваши данные'
    return render_template(
        'users/user_page.html',
        page_title=title,
        user_data=user,
    )


@blueprint.route('/edit_profile', methods=['POST', 'GET'])
@login_required
def edit_profile() -> Response | str:
    form = EditProfForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Изменения внсены')
        return redirect(
            url_for(
                'user.user_page',
                username=current_user.username,
            ),
        )
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template(
        'users/edit_profile.html',
        title='Edit profile',
        form=form,
    )


@blueprint.route('/follow/<username>')
@login_required
def follow(username: str) -> Response:
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found')
        return redirect(url_for('news.index'))
    elif user == current_user:
        flash('You cannot follow yourself')
        return redirect(url_for('user.user_page', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(f'You are following {username}')
    return redirect(url_for('user.user_page', username=username))


@blueprint.route('/unfollow/<username>')
@login_required
def unfollow(username: str) -> Response:
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found')
        return redirect(url_for('news.index'))
    elif user == current_user:
        flash('You cannot unfollow yourself')
        return redirect(url_for('user.user_page', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You are unfollowing {username}')
    return redirect(url_for('user.user_page', username=username))


@blueprint.route('/write_post', methods=['GET', 'POST'])
@login_required
def write_post() -> Response | str:
    post_form = PostForm()
    if post_form.validate_on_submit():
        user = User.query.filter_by(username=current_user.username).first()
        post = Post(body=post_form.post.data, user_id=user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your poem posted')
        return redirect(
            url_for(
                'user.user_page',
                username=current_user.username,
            ),
        )
    title = 'Сочиняй'
    return render_template(
        'users/write_post.html',
        page_title=title,
        form=post_form,
    )
