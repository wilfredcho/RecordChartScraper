import logging
from ChartCSS import ChartCss
from Crawler import Crawler
import charts


def entry():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Started')
    crawl_queue = [ChartCss(chart) for chart in charts.Charts]
    new_songs = []
    for visits in crawl_queue:
        new_songs.extend(Crawler(visits).process())
    print(new_songs)

if __name__ == "__main__":
    entry()
