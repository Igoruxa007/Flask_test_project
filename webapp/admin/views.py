from __future__ import annotations

from flask import Blueprint
from flask_login import current_user

from webapp.user.decorators import admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def admin_index() -> str:
    if current_user.is_admin:
        return 'Hi admin!'
    else:
        return 'You shall not pass'
