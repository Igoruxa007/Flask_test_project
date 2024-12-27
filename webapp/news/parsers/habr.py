from __future__ import annotations

from datetime import datetime

from bs4 import BeautifulSoup

from webapp.model import db
from webapp.news.models import News
from webapp.news.parsers.utils import get_html
from webapp.news.parsers.utils import save_news


def get_news_snippets() -> None:
    html = get_html(
        'https://habr.com/ru/search/?q=python&target_type=posts&order=date',
    )
    # html = get_html_from_file()
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        # with open('Habr.html', 'w', encoding="utf-8") as file:
        #     file.write(html)
        all_news = soup.find(class_='tm-articles-list')
        all_news = all_news.findAll(
            'div', class_='tm-article-snippet tm-article-snippet',
        )
        for news in all_news:
            title = news.find('a', class_='tm-title__link').text
            url = news.find('a', class_='tm-title__link')['href']
            published = news.find('time')['datetime']
            published = parse_habr_date(published)
            save_news(title, url, published)


def parse_habr_date(date_str: str) -> datetime:
    try:
        return datetime.strptime(date_str[:10], '%Y-%m-%d')
    except ValueError:
        return datetime.now()


def get_news_content() -> None:
    news_without_text = News.query.filter(News.text.is_(None))
    for news in news_without_text:
        html = get_html('https://habr.com' + news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            article = soup.find('div', class_='article-formatted-body'). \
                decode_contents()
            if article:
                news.text = article
                db.session.add(news)
                db.session.commit()
