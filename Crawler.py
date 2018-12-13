import requests
import constants
import pandas
import re
from bs4 import BeautifulSoup

class Crawler(object):

    def __init__(self, chart):
        self.chart = chart

    def _get_page(self):
        return requests.get(self.chart.url)

    def _make_soup(self, page):
        return  BeautifulSoup(page.content, 'html.parser') 
    
    def _format(self, string):
        try:
            value = int(re.sub('\s+',' ',string))
        except ValueError:
            value = re.sub('\s+',' ',string)
        return value

    def _proc_row(self, row):
        cur_pos = None
        last_pos = None
        if row.find("span",{"class":self.chart.cur_pos}):
            cur_pos = row.find("span",{"class":self.chart.cur_pos}).text
        if row.find("span",{"class":self.chart.last_pos}):
            last_post = row.find("span",{"class":self.chart.last_pos}).text
        if bool(cur_pos) and bool(last_post):
            return (self._format(cur_pos), self._format(last_post))

    def run(self):
        page = self._get_page()
        if page.status_code == constants.OK:
            soup = self._make_soup(page)
            chart = soup.find("table",{"class":self.chart.table})
            rows = chart.find_all('tr')
            results = [self._proc_row(row) for row in rows if bool(self._proc_row(row))]
        print(results)
            

