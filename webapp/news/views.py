from flask import abort, Blueprint, current_app, render_template

from webapp.weather import weather_by_city
from webapp.news.models import News

blueprint = Blueprint('news', __name__)

@blueprint.route("/")
def index():
    page_title = "Прогноз погоды"
    weather = weather_by_city()
    print(weather)
    news = News.query.order_by(News.published.desc()).all()
    return render_template('news/index.html', 
        page_title=page_title, 
        weather_text=weather,
        news_list=news
        )

@blueprint.route('/news/<int:news_id>')
def single_news(news_id):
    my_news = News.query.filter(News.id == news_id).first()
    if not my_news:
        abort(404)
    return render_template('news/single_news.html', page_title=my_news.title, news=my_news)
