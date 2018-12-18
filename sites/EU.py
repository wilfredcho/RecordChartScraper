from sites.common.util import format_text, proc_info
import itertools
from sites.Base import Base

class EU(Base):

    def proc_row(self, row, chart):
        list_product = itertools.product(chart.cur_pos, chart.last_pos, chart.artist_title)
        for cur_pos, last_pos, artist_title in list_product:
            if row.find_all("td", {"class": cur_pos}):
                import pdb; pdb.set_trace()
                for sub_row in row.find_all("td", {"class": cur_pos}):
                    if sub_row.findNext("td", {"class":cur_pos}):
                        cur_pos = format_text(sub_row.findNext("td", {"class":cur_pos}).text)
                        if sub_row.findNext("td", {"class": chart.last_pos}):
                            last_pos = format_text(sub_row.findNext("td", {"class": chart.last_pos}).text)
                            if sub_row.findNext("td", {"class": artist_title}):
                                artist, title = row.findNext("td", {"class": artist_title}).text.split(' - ')
                                print(chart, cur_pos, last_pos, title, artist)
                                return proc_info(chart, cur_pos, last_pos, title, artist)


    def run(self, soup, chart):
        table = soup.find("table")
        rows = table.find_all('tr')
        return [self.proc_row(row, chart) for row in rows if bool(self.proc_row(row, chart))]
