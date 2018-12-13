import requests
import constants

class Crawler(object):

    def __init__(self, chart):
        self.chart = chart

    def _get_page(self):
        return requests.get(chart.url)

    def _make_soup(self, page)
    
    def run(self):
        page = self._get_page()
        if page.status_code == constants.OK:
            self._

