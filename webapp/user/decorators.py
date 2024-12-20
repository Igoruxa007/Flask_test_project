from __future__ import annotations

from functools import wraps

from flask import current_app
from flask import flash
from flask import redirect
from flask import request
from flask import url_for
from flask_login import config
from flask_login import current_user


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in config.EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.config.get('LOGIN_DISABLED'):
            return func(*args, **kwargs)
        elif not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not current_user.is_admin:
            flash('This page is only available to admins')
            return redirect(url_for('news.index'))
        return func(*args, **kwargs)
    return decorated_view
