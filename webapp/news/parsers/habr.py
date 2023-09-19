from datetime import datetime, timedelta

from bs4 import BeautifulSoup

from webapp.news.parsers.utils import get_html, save_news

def get_news_snippets():
    html = get_html("https://habr.com/ru/search/?target_type=posts&q=python&order_by=date")
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        all_news = soup.find(class_ = "tm-articles-list").findAll('div', class_='tm-article-snippet tm-article-snippet')
        for news in all_news:
            title = news.find('a', class_='tm-title__link').text
            url = news.find('a', class_='tm-title__link')['href']
            published = news.find('time')['datetime']
            # published = parse_habr_date(published)
            print(title, url, published)
            # save_news(title, url, published)

def parse_habr_date(date_str):
    if 'сегодня' in date_str:
        today = datetime.now()
        date_str = date_str.replace('сегодня', today.strftime('%d %B %Y'))
    elif 'вчера' in date_str:
        yesterday = datetime.now() - timedelta(days=1)
        date_str = date_str.replace('вчера', yesterday.strftime('%d %B %Y'))
    try:
        return datetime.strptime(date_str, '%d %B %Y в %H:%M')
    except ValueError:
        return datetime.now()