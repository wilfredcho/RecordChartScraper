import logging
from ChartCSS import ChartCss
from Crawler import Crawler
import charts
import csv
from sites.common.util import fuzzy_match
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime

def get_Chart(visits):
     return Crawler(visits).process()

def remove_duplicate(song_list):
    #for song in song_list
    return song_list
def to_file(song_list):
    with open(datetime.now().strftime("%Y_%m_%d")+'.csv','w') as out:
        csv_out=csv.writer(out)
        csv_out.writerow(['artisit','title'])
        for row in song_list:
            csv_out.writerow(row)

def entry():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='process.log', level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info('Started')
    crawl_queue = [ChartCss(chart) for chart in charts.Charts]
    new_songs = []
    with ProcessPoolExecutor() as executor:
        for new_list in executor.map(get_Chart, crawl_queue):
                new_songs.extend(new_list)
    to_file(remove_duplicate(new_songs))
    logger.info('Ended')

if __name__ == "__main__":
    entry()
