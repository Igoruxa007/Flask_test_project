from datetime import datetime

from bs4 import BeautifulSoup

from webapp.news.parsers.utils import get_html, save_news
from webapp.model import db
from webapp.news.models import News

def get_news_snippets():
    html = get_html("https://habr.com/ru/search/?target_type=posts&q=python&order_by=date")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find(class_ = "tm-articles-list").findAll('div', class_='tm-article-snippet tm-article-snippet')
        for news in all_news:
            title = news.find('a', class_='tm-title__link').text
            url = news.find('a', class_='tm-title__link')['href']
            published = news.find('time')['datetime']
            published = parse_habr_date(published)
            save_news(title, url, published)

def parse_habr_date(date_str):
    try:
        return datetime.strptime(date_str[:10], '%Y-%m-%d')
    except ValueError:
        return datetime.now()

def get_news_content():
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_html('https://habr.com'+news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            article = soup.find('div', class_='article-formatted-body').decode_contents()
            if article:
                news.text = article
                db.session.add(news)
                db.session.commit()