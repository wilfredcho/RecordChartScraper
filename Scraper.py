import logging
import pickle
import re
import time
from importlib import import_module

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

import sites.common.constants as constants
from config import VISITED_SONGS
from sites import *
from sites.common.util import Singleton

logger = logging.getLogger('process')


class LoadFiles(object):
    __metaclass__ = Singleton

    def __init__(self):
        try:
            with open(VISITED_SONGS, "rb") as f:
                self.old_songs = pickle.load(f)
        except BaseException:
            self.old_songs = []


FILES = LoadFiles()


class Scraper(object):

    def __init__(self, chart):
        self.chart = chart
        setattr(self.chart, 'dislike_artist', constants.DISLIKE_ARTIST)
        setattr(self.chart, 'dislike_title', constants.DISLIKE_TITLE)
        setattr(self, 'run', getattr(import_module(
            'sites.' + self.chart.co), self.chart.co)().run)
        setattr(self.chart, 'old_songs', FILES.old_songs)

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
            try:
                return self.run(soup, self.chart)
            except Exception:
                logging.error("Failed to visit " +
                              self.chart.url)
                logger.exception("Exception: ")
                return None
        else:
            logging.error("Failed to visit : " +
                          str(self.page.status_code) + " : " + self.chart.url)
            return None
