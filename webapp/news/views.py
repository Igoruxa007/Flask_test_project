from flask import abort, Blueprint, render_template, request
from flask_login import current_user, login_required

from webapp.weather import weather_by_city
from webapp.news.models import News

blueprint = Blueprint('news', __name__)


@blueprint.route('/')
@blueprint.route('/index')
def index():
    page_title = "Прогноз погоды"
    weather = weather_by_city()
    news = News.query.order_by(News.published.desc()).all()
    posts = None
    if current_user.is_authenticated:
        posts = current_user.followed_posts().paginate(page=1,
                                                       per_page=5,
                                                       error_out=False).items
    return render_template('news/index.html',
                           page_title=page_title,
                           weather_text=weather,
                           news_list=news,
                           posts=posts
                           )


@blueprint.route('/explore')
@login_required
def explore():
    page_title = "Прогноз погоды"
    weather = weather_by_city()
    news = News.query.order_by(News.published.desc()).all()

    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page=page, per_page=5, error_out=False).items
    return render_template('news/index.html',
                           page_title=page_title,
                           weather_text=weather,
                           news_list=news,
                           posts=posts
                           )

@blueprint.route('/news/<int:news_id>')
def single_news(news_id):
    my_news = News.query.filter(News.id == news_id).first()
    if not my_news:
        abort(404)
    return render_template('news/single_news.html',
                           page_title=my_news.title,
                           news=my_news)
