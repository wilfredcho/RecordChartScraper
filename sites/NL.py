from sites.common.util import format_text, proc_info
from sites.Base import Base

class NL(Base):
    def proc_row(self, row, chart):
        cur_pos = format_text(row.find_all("td", {"class":"text"})[0].text)
        last_pos = format_text(row.find_all("td")[1].text)
        if last_pos:
            artist_title = row.find("a", {"class":"navb"}).text
            artist = row.find("a", {"class":"navb"}).select("b")[0].text
            title = artist_title.replace(artist, "")
            print(chart, cur_pos, last_pos, title, artist)
            return proc_info(chart, cur_pos, last_pos, title, artist)


    def run(self, soup, chart):
        table = soup.find("table")
        rows = table.find_all("tr", {"class":"charts"})
        return [self.proc_row(row, chart) for row in rows if bool(self.proc_row(row, chart))]
