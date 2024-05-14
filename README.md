# Flask_test_project

В файле config.py прописать:
SQLALCHEMY_DATABASE_URI
WEATHER_API_KEY для weatherapi.com
WEATHER_DEFAULT_CITY
SECRET_KEY
SQLALCHEMY_TRACK_MODIFICATIONS = False - отключение отслеживания изменений в БД
 
Для обновления новостей зпустить get_all_news.py
Для добавления админа create_admin.py

flask db init
flask db migrate -m "Comment"
set FLASK_APP=webapp && flask db upgrade

Для запуска сервера на windows:
set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run
Linux:
export FLASK_APP=webapp && export FLASK_DEBUG=1 && flask run