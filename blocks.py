import compare
import re
from Info import Info
from bs4 import BeautifulSoup

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

def AU_proc_row(row, chart):
    if row.find("td", {"class": "ranking"}):
        cur_pos = format_text(row.find("td", {"class": "ranking"}).text)
        try:
            int(cur_pos)
        except ValueError:
            cur_pos = ''.join(char for char in cur_pos if char.isdigit())
        last_pos = format_text(row.find("td", {"class": "chart-grid-column"}).text)
        if last_pos:
            sub_post = row.find("td", {"class": "title-artist"})
            title = format_text(sub_post.find("div", {"class": "item-title"}).text)
            artist = format_text(sub_post.find("div", {"class": "artist-name"}).text)
            return proc_info(chart, cur_pos, last_pos, title, artist)


def AU_run(soup, chart):
    table = soup.find("table", {"id": "tbChartItems"})
    rows = table.find_all('tr')
    return [AU_proc_row(row, chart) for row in rows if bool(AU_proc_row(row, chart))]


def FR_proc_row(row, chart):

    cur_pos = format_text(row.find("span", {"itemprop": "position"}).text)
    last_pos = row.find("span", {"class": "Sub subStatsPrev"}).text
    last_pos = format_text(''.join(char for char in last_pos if char.isalnum()))
    title_artist = row.find_all("span", {"itemprop":"name"})
    title = title_artist[0].text
    artist = ''.join(artist.text for artist in title_artist[1:])
    return proc_info(chart, cur_pos, last_pos, title, artist)


def FR_run(soup, chart):
    table = soup.find("table", {"id": "ChartTable"})
    rows = table.find_all("tr" , {"itemprop":"itemListElement"})
    return [FR_proc_row(row, chart) for row in rows if bool(FR_proc_row(row, chart))]


def NL_proc_row(row, chart):
    cur_pos = format_text(row.find_all("td", {"class":"text"})[0].text)
    last_pos = format_text(row.find_all("td")[1].text)  
    artist_title = row.find("a", {"class":"navb"}).text
    artist = row.find("a", {"class":"navb"}).select("b")[0].text
    title = artist_title.replace(artist, "")
    return proc_info(chart, cur_pos, last_pos, title, artist)


def NL_run(soup, chart):
    table = soup.find("table")
    rows = table.find_all("tr", {"class":"charts"})
    return [NL_proc_row(row, chart) for row in rows if bool(NL_proc_row(row, chart))]

def EU_proc_row(row, chart):
    import pdb; pdb.set_trace()
    if row.find("td", {"class": chart.cur_pos}):
        cur_pos = format_text(row.find("td", {"class": chart.cur_pos}).text)
        try:
            last_pos = format_text(row.find("td", {"class": chart.last_pos_0}).text)
            artist, title = row.find("td", {"class": chart.artist_title_0}).text.split(' - ')
            return proc_info(chart, cur_pos, last_pos, title, artist)
        except AttributeError:
            try:
                last_pos = format_text(row.find("td", {"class": chart.last_pos}).text)
            except Exception:
                import pdb; pdb.set_trace()
                print()
            artist, title = row.find("td", {"class": chart.artist_title}).text.split(' - ')
            return proc_info(chart, cur_pos, last_pos, title, artist)


def EU_run(soup, chart):
    table = soup.find("table")
    rows = table.find_all('tr')
    return [EU_proc_row(row, chart) for row in rows if bool(EU_proc_row(row, chart))]
