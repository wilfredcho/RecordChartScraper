import logging
from ChartCSS import ChartCss
from Crawler import Crawler
import charts


def entry():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    logger.info('Started')
    crawl_queue = [ChartCss(chart) for chart in charts.Charts]
    for visits in crawl_queue:
        Crawler(visits).process()


if __name__ == "__main__":
    entry()
