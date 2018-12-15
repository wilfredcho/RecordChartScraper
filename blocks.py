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

def proc_info(chart, cur_pos, last_pos, title, artist):
    info = Info(cur_pos, last_pos, title, artist)
    if condit(info, chart):
        return (cur_pos, last_pos, artist, title)

def UK_proc_row(row, chart):
    if row.find("span", {"class": "position"}):
        cur_pos = format_text(row.find("span", {"class": "position"}).text)
        last_pos = format_text(row.find("span", {"class": "last-week"}).text)
        sub_post = row.find("div", {"class": "title-artist"})
        title = format_text(sub_post.find("div", {"class": "title"}).text)
        artist = format_text(sub_post.find("div", {"class": "artist"}).text)
        return proc_info(chart, cur_pos, last_pos, title, artist)


def UK_run(soup, chart):
    table = soup.find("table", {"class": "chart-positions"})
    rows = table.find_all('tr')
    return [UK_proc_row(row, chart) for row in rows if bool(UK_proc_row(row, chart))]


def DK_proc_row(row, chart):
    if row.find("div", {"id": "denneuge"}):
        cur_pos = format_text(row.find("div", {"id": "denneuge"}).text)
        last_pos = format_text(row.find("div", {"id": "sidsteuge"}).text)
        sub_post = row.findNext("div", {"id": "udgivelse"})
        title = format_text(sub_post.find("div", {"id": "titel"}).text)
        artist = format_text(sub_post.find("div", {"id": "artistnavn"}).text)
        return proc_info(chart, cur_pos, last_pos, title, artist)
    if row.find("div", {"id": "denneugeny"}):
        cur_pos = format_text(row.find("div", {"id": "denneugeny"}).text)
        last_pos = format_text(row.find("div", {"id": "sidsteuge"}).text)
        sub_post = row.findNext("div", {"id": "udgivelse"})
        title = format_text(sub_post.find("div", {"id": "titel"}).text)
        artist = format_text(sub_post.find("div", {"id": "artistnavn"}).text)
        return proc_info(chart, cur_pos, last_pos, title, artist)

def DK_run(soup, chart):
    rows = soup.find_all("div", {"id": "linien"})
    return [DK_proc_row(row, chart) for row in rows if bool(DK_proc_row(row, chart))]