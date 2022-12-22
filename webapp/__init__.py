from flask import Flask, render_template

from webapp.python_org_news import get_python_news
from webapp.weather import weather_by_city

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def index():
        page_title = "Прогноз погоды"
        weather = weather_by_city("Moscow")
        news = get_python_news()
        return render_template('index.html', 
                                page_title=page_title, 
                                weather_text=weather,
                                news_list=news
                                )
    return app