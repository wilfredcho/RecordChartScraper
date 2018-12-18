from sites.common.util import format_text, proc_info
import itertools
from sites.Base import Base

class EU(Base):

    def proc_row(self, row, chart):
        info = []
        for col in chart.offset:
            cells = row.find_all("td")
            try:
                cur_pos = format_text(cells[chart.cur_pos+col].text)
            except Exception:
                continue
            last_pos = format_text(cells[chart.last_pos+col].text)
            try:
                artist, title = cells[chart.artist_title+col].text.split(' - ')
            except Exception:
                try:
                    artist, title = cells[chart.artist_title+col].text.split(' -\n ')
                except Exception:
                    import pdb; pdb.set_trace()
                    print()
            if bool(proc_info(chart, cur_pos, last_pos, title, artist)):
                info.append(proc_info(chart, cur_pos, last_pos, title, artist))
        return info

    def run(self, soup, chart):
        table = soup.find("table")
        rows = table.find_all('tr')
        rows = rows[chart.start_row:chart.end_row]
        info = []
        for idx, row in enumerate(rows):
            print(idx)
            info.extend(self.proc_row(row, chart))

        return info