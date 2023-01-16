from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user

from webapp.forms import LoginForm
from webapp.model import db, News, User
from webapp.weather import weather_by_city

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Получение ID пользователся для при загрузке страниц
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/")
    def index():
        page_title = "Прогноз погоды"
        weather = weather_by_city(app.config["WEATHER_DEFAULT_CITY"])
        news = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', 
            page_title=page_title, 
            weather_text=weather,
            news_list=news
            )
    
    @app.route('/login')
    def login():
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)
    
    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash('Вы вошли на сайт')
                return redirect(url_for('index'))
        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))

    return app