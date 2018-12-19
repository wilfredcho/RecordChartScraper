import requests
import sites.common.constants as constants
import re
from bs4 import BeautifulSoup
from sites import *
import time
from selenium import webdriver
from importlib import import_module
import logging

class Crawler(object):
    mod = __import__('sites', fromlist=['UK'])

    def __init__(self, chart):
        self.chart = chart
        setattr(self.chart, 'dislike_artist', constants.DISLIKE_ARTIST)
        setattr(self.chart, 'dislike_title', constants.DISLIKE_TITLE)
        setattr(self, 'run', getattr(import_module('sites.'+self.chart.co), self.chart.co)().run)

    def _get_page(self):
        return requests.get(self.chart.url)

    def _make_soup(self):
        return BeautifulSoup(self.page.content, 'html.parser')

    def _make_js_soup(self):
        driver = webdriver.Chrome()
        driver.get(self.chart.url)
        time.sleep(constants.WAIT)
        soup = driver.page_source
        driver.quit()
        return BeautifulSoup(soup, 'html.parser')


    def process(self):
        self.page = self._get_page()
        if self.page.status_code == constants.OK:
            if self.chart.js:
                soup = self._make_js_soup()
            else:
                soup = self._make_soup()
            return self.run(soup, self.chart)
        else:
            logging.ERROR("Failed to visit " + self.chart.url)