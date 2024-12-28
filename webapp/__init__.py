from __future__ import annotations

from datetime import datetime
from datetime import timezone

from flask import Flask
from flask_login import current_user
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment

from webapp.admin.views import blueprint as admin_blueprint
from webapp.errors import internal_error
from webapp.errors import not_found_error
from webapp.model import db
from webapp.news.views import blueprint as news_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_pyfile('config.py')
        db.init_app(app)
        with app.app_context():
            db.create_all()
    else:
        app.config.from_mapping(test_config)
        db.init_app(app)
        with app.app_context():
            db.create_all()

    migrate = Migrate(app, db)

    moment = Moment(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(news_blueprint)

    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_error)

    # Получение ID пользователся для при загрузке страниц
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.before_request
    def before_request():
        if current_user.is_authenticated:
            current_user.last_seen = datetime.now(tz=timezone.utc)
            db.session.add(current_user)
            db.session.commit()

    return app
