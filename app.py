import logging
from ChartCSS import ChartCss
from Crawler import Crawler
import charts
from concurrent.futures imoport ProcessPoolExecutor

def get_Chart(visits):
     return Crawler(visits).process()

def entry():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Started')
    crawl_queue = [ChartCss(chart) for chart in charts.Charts]
    new_songs = []
    with ProcessPoolExecutor() as executor:
        for chart, new_list in zip(PRIMES, executor.map(get_Chart, crawl_queue)):
                new_songs.extend(new_list)
    print(new_songs)

if __name__ == "__main__":
    entry()
