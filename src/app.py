from webapp2 import WSGIApplication, Route
from settings import *
from src.main import main


wsgi = WSGIApplication(
    [
        Route(r'/cron/scrape', name='scrape', handler=main.Scrape),
        Route(r'/', name='home', handler=main.Index),
    ],
    debug=DEBUG,
    config=CONFIG
)