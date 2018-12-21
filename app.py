import csv
import logging
import pickle
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime

import charts
from ChartCSS import ChartCss
from config import LOG_NAME, MULTIPROC, VISITED_SONGS
from Scraper import Scraper
from sites.common.util import fuzzy_match
from tool.llist import LinkedList


def get_Chart(visits):
    return Scraper(visits).process()


def remove_duplicate(song_list):
    if song_list:
        llist = LinkedList(song_list)
        song = llist.head
        song_list = []
        while song and song.next:
            next_song = song
            while next_song.next:
                first = song.value[0] + song.value[1]
                second = next_song.next.value[0] + next_song.next.value[1]
                if fuzzy_match(first, second):
                    next_song.next = next_song.next.next
                else:
                    next_song = next_song.next
            song_list.append(song.value)
            song = song.next
        return song_list
    return []


def to_file(song_list):
    with open(datetime.now().strftime("%Y_%m_%d") + '.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['artist', 'title'])
        for row in song_list:
            csv_out.writerow(row)


def entry():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename=LOG_NAME, level=logging.INFO)
    start = time.time()
    logger.info('Started')
    crawl_queue = [ChartCss(chart) for chart in charts.Charts]
    new_songs = []
    if MULTIPROC:
        with ProcessPoolExecutor() as executor:
            for new_list in executor.map(get_Chart, crawl_queue):
                if new_list:
                    new_songs.extend(new_list)
    else:
        for chart in crawl_queue:
            new_list = get_Chart(chart)
            if new_list:
                new_songs.extend(new_list)
    new_songs = remove_duplicate(new_songs)
    to_file(new_songs)
    end = time.time()
    logger.info('Ended: Run time ' + str(end - start) + 's')
    with open(VISITED_SONGS, 'wb') as f:
        pickle.dump(new_songs, f)


if __name__ == "__main__":
    entry()
