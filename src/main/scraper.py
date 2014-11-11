import logging
import requests
import re
from bs4 import BeautifulSoup
from src.main.models import House
from src.settings import REGIONS, PARENT_KEY
from google.appengine.ext import ndb


class Scraper():
    url_base = 'http://www.realestate.com.au'
    url_buy_houses = '{0}/buy/property-house-in-{1}/list-{2}?activeSort=list-date'


    def __init__(self):
        from google.appengine.api import urlfetch
        urlfetch.set_default_fetch_deadline(60)


    def run(self):
        for region in REGIONS:
            page = 1
            isFinished = False
            while not isFinished:
                logging.info('Region {0} page {1}'.format(region, page))
                url = self.url_buy_houses.format(self.url_base, region, page)
                logging.debug('Scraping {0}'.format(url))
                res = requests.get(url)
                res.raise_for_status()
                data = self.parseList(region, res.content)
                if not data:
                    logging.warn('{0}: No more data found!'.format(region))
                    break
                isFinished = self.saveData(data)
                page += 1


    def scrapeDetail(self, link):
        s = requests.Session()
        a = requests.adapters.HTTPAdapter(max_retries=3)
        s.mount('http://', a)
        # logging.info('>>> scrapeDetail >>> ' + str(link))
        res = s.get(link, timeout=10)
        res.raise_for_status()
        return res.content


    def parseList(self, region, content):
        data = []
        soup = BeautifulSoup(content)
        for resultBody in soup.find_all('div', class_='resultBody'):
            # print resultBody.prettify().encode('utf8')
            item = {}
            item['region'] = region
            item['url'] = resultBody.find('a', class_='detailsButton')['href']
            item['name'] = resultBody.find('a', class_='name').text
            item['title'] = resultBody.find('h3', class_='title').text
            item['description'] = resultBody.find('p', class_='description').text
            item['img'] = resultBody.find('div', class_='photoviewer').find('img')['src']
            # property features
            propertyFeatures = resultBody.find('ul', class_='propertyFeatures')
            bedrooms = propertyFeatures.find('img', alt='Bedrooms')
            item['bedrooms'] = int(bedrooms.find_next('span').text) if bedrooms else None
            bathrooms = propertyFeatures.find('img', alt='Bathrooms')
            item['bathrooms'] = int(bathrooms.find_next('span').text) if bathrooms else None
            car_spaces = propertyFeatures.find('img', alt='Car Spaces')
            item['car_spaces'] = int(car_spaces.find_next('span').text) if car_spaces else None
            # agent
            item['agent'] = None
            logo = resultBody.find('img', class_='logo')
            if logo:
                item['agent'] = logo['alt']
            else:
                listerName = resultBody.find('p', class_='listerName')
                if listerName:
                    item['agent'] = listerName.find('span').text
            # price
            priceText = resultBody.find('span', class_='priceText')
            item['info'] = priceText.text if priceText else ''
            priceGroups = re.search(r'\$(\d+)', item['info'].replace(',', ''), re.U)
            item['price'] = None if not priceGroups else int(priceGroups.group(1))
            data.append(item)
            # logging.info(item)
        logging.info('ParseList: {0} items found'.format(len(data)))
        return data


    @ndb.transactional(retries=0)
    def saveData(self, data):
        isFinished = True
        for item in data:
            house = House.get_by_id(item['url'], parent=PARENT_KEY)
            if not house:
                house = House(**item)
                isFinished = False
            else:
                house.populate(**item)

            key = house.put()
            logging.info('House: {0}'.format(key))

        logging.info('Is finished: {0}'.format(isFinished))
        return isFinished