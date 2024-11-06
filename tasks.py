from celery import Celery
from celery.schedules import crontab

from webapp import create_app
from webapp.news.parsers import habr

falsk_app = create_app()
celery_app = Celery("tasks", broker="redis://localhost:6379/0")


@celery_app.task
def habr_snippets():
    with falsk_app.app_context():
        habr.get_news_snippets()


@celery_app.task
def habr_content():
    with falsk_app.app_context():
        habr.get_news_content()


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="*/10"), habr_snippets.s())
    sender.add_periodic_task(crontab(minute="*/10"), habr_content.s())
