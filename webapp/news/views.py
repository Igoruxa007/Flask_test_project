from flask import abort, Blueprint, render_template, request, flash
from flask_login import current_user, login_required

from webapp.model import db
from webapp.weather import weather_by_city
from webapp.news.models import News
from webapp.user.models import Post
from webapp.user.forms import PostForm

blueprint = Blueprint('news', __name__)


@blueprint.route('/', methods=['GET', 'POST'])
@blueprint.route('/index', methods=['GET', 'POST'])
def index():
    page_title = "Прогноз погоды"
    weather = weather_by_city()
    news = News.query.order_by(News.published.desc()).all()
    posts = None
    form = None
    if current_user.is_authenticated:
        posts = current_user.followed_posts().paginate(page=1,
                                                       per_page=5,
                                                       error_out=False).items
        form = PostForm()
        if form.validate_on_submit():
            post = Post(body=form.post.data)
            db.session.add(post)
            db.session.commit()
            flash('Post posted!')

    return render_template('news/index.html',
                           page_title=page_title,
                           weather_text=weather,
                           news_list=news,
                           posts=posts,
                           form=form
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
