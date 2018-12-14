import requests
import constants
import re
from bs4 import BeautifulSoup
import util
from Info import Info

class Crawler(object):

    def __init__(self, chart):
        self.chart = chart

    def _get_page(self):
        return requests.get(self.chart.url)

    def _make_soup(self, page):
        return  BeautifulSoup(page.content, 'html.parser') 
    
    def _format(self, string):
        try:
            value = int(re.sub('\s+','',string))
        except ValueError:
            value = re.sub('\s+','',string)
        return value

    def _proc_row(self, row):
        if row.find("span",{"class":self.chart.cur_pos}):
            cur_pos = self._format(row.find("span",{"class":self.chart.cur_pos}).text)
            last_pos = self._format(row.find("span",{"class":self.chart.last_pos}).text)
            sub_post = row.find("div", {"class":"title-artist"})
            title = self._format(sub_post.find("div",{"class":"title"}).text)
            artist = self._format(sub_post.find("div",{"class":"artist"}).text)
            row_info = Info(cur_pos, last_pos, title, artist)
            if  self._condit(row_info):
                return (cur_pos, last_pos, artist, title)

    def _condit(self, info):
        return all([getattr(util, condit)(info, val) for condit, val in self.chart.condit.items() if val])
    
    def run(self):
        page = self._get_page()
        if page.status_code == constants.OK:
            soup = self._make_soup(page)
            chart = soup.find("table",{"class":self.chart.table})
            rows = chart.find_all('tr')
            results = [self._proc_row(row) for row in rows if bool(self._proc_row(row))]
        print(results)
            
