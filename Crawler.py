import requests
import constants
import re
from bs4 import BeautifulSoup
import compare
from Info import Info
import blocks

class Crawler(object):

    def __init__(self, chart):
        self.chart = chart
        setattr(self, 'run', getattr(blocks, self.chart.co + '_run'))

    def _get_page(self):
        return requests.get(self.chart.url)

    def _make_soup(self, page):
        return BeautifulSoup(page.content, 'html.parser')

    def process(self):
        page = self._get_page()
        if page.status_code == constants.OK:
            soup = self._make_soup(page)
            results = self.run(soup, self.chart)
            print(results)
