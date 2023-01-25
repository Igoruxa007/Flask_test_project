from flask import Blueprint, current_app
from flask import render_template

from webapp.weather import weather_by_city
from webapp.news.models import News

blueprint = Blueprint('news', __name__)

@blueprint.route("/")
def index():
    page_title = "Прогноз погоды"
    weather = weather_by_city(current_app.config["WEATHER_DEFAULT_CITY"])
    news = News.query.order_by(News.published.desc()).all()
    return render_template('index.html', 
        page_title=page_title, 
        weather_text=weather,
        news_list=news
        )