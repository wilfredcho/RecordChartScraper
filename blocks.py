import compare
import re
from Info import Info


def condit(info, chart):
    return all([getattr(compare, condit)(info, val)
                for condit, val in chart.condit.items() if val])


def format_text(text):
    try:
        value = int(re.sub(r'\s+', '', text))
    except ValueError:
        value = re.sub(r'\s+', '', text)
    return value


def UK_proc_row(row, chart):
    if row.find("span", {"class": chart.cur_pos}):
        cur_pos = format_text(row.find("span", {"class": chart.cur_pos}).text)
        last_pos = format_text(
            row.find(
                "span", {
                    "class": chart.last_pos}).text)
        sub_post = row.find("div", {"class": "title-artist"})
        title = format_text(sub_post.find("div", {"class": "title"}).text)
        artist = format_text(sub_post.find("div", {"class": "artist"}).text)
        info = Info(cur_pos, last_pos, title, artist)
        if condit(info, chart):
            return (cur_pos, last_pos, artist, title)


def UK_run(soup, chart):
    table = soup.find("table", {"class": chart.table})
    rows = table.find_all('tr')
    results = [
        UK_proc_row(
            row,
            chart) for row in rows if bool(
            UK_proc_row(
                row,
                chart))]
    return results


def DK_run(soup, chart):
    for content in soup.find_all("div", {"id": "linien"}):
        content.findNext("div", {"id": "udgivelse"})
    return results
