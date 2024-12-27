from __future__ import annotations

from typing import Any
from typing import Literal

from flask import render_template

from webapp.model import db


def not_found_error(error: Any) -> tuple[str, Literal[404]]:
    return render_template('errors/404.html'), 404


def internal_error(error: Any) -> tuple[str, Literal[500]]:
    db.session.rollback()
    return render_template('errors/500.html'), 500
