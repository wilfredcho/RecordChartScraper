import concurrent.futures
import csv
import logging
import pickle
import time
from datetime import datetime
from os.path import isfile

import charts
from ChartCSS import ChartCss
from config import LOG_NAME, MULTIPROC, VISITED_SONGS
from Scraper import Scraper
from sites.common.util import fuzzy_match
from tool.llist import LinkedList
from tool.logger import setup_logger

setup_logger('process', LOG_NAME)


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
                first = str(song.value[0]) + " " + str(song.value[1])
                second = str(
                    next_song.next.value[0]) + str(next_song.next.value[1])
                if fuzzy_match(first, second):
                    next_song.next = next_song.next.next
                else:
                    next_song = next_song.next
            song_list.append(song.value)
            song = song.next
        return song_list
    return []


def to_file(song_list):
    sequence = ""
    filename = datetime.now().strftime("%Y_%m_%d") + "_%s.csv"
    while isfile(filename % sequence):
        sequence = int(sequence or 0) + 1
    filename = filename % sequence
    with open(filename, 'w') as out:
        csv_out = csv.writer(out)
        #csv_out.writerow(['artist', 'title'])
        for row in song_list:
            csv_out.writerow(row)


def entry():
    logger = logging.getLogger('process')
    start = time.time()
    logger.info('Started')
    try:
        with open(VISITED_SONGS, 'rb') as f:
            old_songs = pickle.load(f)
    except:
        old_songs = []
    crawl_queue = [ChartCss(chart) for chart in charts.Charts]
    new_songs = []
    if MULTIPROC:
        with concurrent.futures.ProcessPoolExecutor() as executor:
            future_to_url = (executor.submit(
                get_Chart, crawl) for crawl in crawl_queue)
            for new_list in concurrent.futures.as_completed(future_to_url):
                if new_list.result():
                    new_songs.extend(new_list)
    else:
        for chart in crawl_queue:
            print(chart.url)
            new_list = get_Chart(chart)
            if new_list:
                new_songs.extend(new_list)
    new_songs = remove_duplicate(new_songs)
    to_file(new_songs)
    end = time.time()
    with open(VISITED_SONGS, 'wb') as f:
        pickle.dump(new_songs + old_songs, f)
    logger.info('Ended: Run time ' + str(end - start) + 's')


if __name__ == "__main__":
    entry()
