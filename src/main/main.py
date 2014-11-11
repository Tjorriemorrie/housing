from webapp2 import RequestHandler
from src.handlers import BaseHandler
from src.settings import JINJA_ENVIRONMENT, DEBUG
from src.main.scraper import Scraper


class Index(RequestHandler):
    def get(self):
        template_values = {
            'nav': 'home',
        }
        template = JINJA_ENVIRONMENT.get_template('main/templates/index.html')
        self.response.write(template.render(template_values))


class Scrape(RequestHandler):
    def get(self):
        scraper = Scraper()
        scraper.run()
        self.response.write('OK')