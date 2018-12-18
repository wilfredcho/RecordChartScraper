from sites.common.util import format_text, proc_info
from sites.Base import Base

class SE(Base):
    def proc_trow(self, row, chart):
        cur_pos = format_text(row.find_all("td")[0].text)
        last_pos = format_text(row.find("span", {"class":"fgpl"}).text)
        last_pos = last_pos[last_pos.find("[")+1:last_pos.find("]")]
        artist = format_text(row.find("span", {"class":"artist"}).text)
        title = format_text(row.find("span", {"class":"title"}).text)
        return proc_info(chart, cur_pos, last_pos, title, artist)

    def proc_row(self, row, chart):
        cur_pos = format_text(row.find_all("td")[0].text)
        last_pos = format_text(row.find("span", {"class":"fgpl"}).text)
        artist = format_text(row.find("span", {"class":"artist"}).text)
        title = format_text(row.find("span", {"class":"title"}).text)
        return proc_info(chart, cur_pos, last_pos, title, artist)

    def run(self, soup, chart):
        top = soup.find("table", {"class":"toppos"})
        top_row = top.find_all("tr")
        top_row = [self.proc_trow(row, chart) for row in top_row if bool(self.proc_trow(row, chart))]
        table = soup.find("table", {"class":"charttable"}).find("tbody")
        rows = table.find_all("tr")
        return top_row + [self.proc_row(row, chart) for row in rows if bool(self.proc_row(row, chart))]
