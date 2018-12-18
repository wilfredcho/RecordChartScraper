import sites.common.compare as compare
import re
from sites.common.Info import Info

def condit(info, chart):
    return all([getattr(compare, condit)(info, val)
                for condit, val in chart.condit.items() if val])


def format_text(text):
    if text:
        try:
            value = int(re.sub(r'\s+', '', text))
        except ValueError:
            value = re.sub(r'\s+', '', text)
        return value

def proc_info(chart, cur_pos, last_pos, title, artist):
    info = Info(cur_pos, last_pos, title, artist)
    if condit(info, chart):
        return (cur_pos, last_pos, artist, title)