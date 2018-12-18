import requests
import sites.common.constants as constants
import re
from bs4 import BeautifulSoup
from sites import *
import time
from selenium import webdriver
from importlib import import_module

class Crawler(object):
    mod = __import__('sites', fromlist=['UK'])

    def __init__(self, chart):
        self.chart = chart
        setattr(self, 'run', getattr(import_module('sites.'+self.chart.co), self.chart.co)().run)

    def _get_page(self):
        return requests.get(self.chart.url)

    def _make_soup(self, page):
        return BeautifulSoup(page.content, 'html.parser')

    def _make_js_soup(self):
        driver = webdriver.Chrome()
        driver.get(self.chart.url)
        time.sleep(constants.WAIT)
        soup = driver.page_source
        driver.quit()
        return BeautifulSoup(soup, 'html.parser')


    def process(self):
        page = self._get_page()
        if page.status_code == constants.OK:
            if self.chart.js:
                soup = self._make_js_soup()
            else:
                soup = self._make_soup(page)
            results = self.run(soup, self.chart)
            print(results)