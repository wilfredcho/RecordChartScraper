## Record Chart Scraper
A web scraper that grabs new music titles from around the world from targeted music charts. Focus on getting new songs and songs that entered the desired position. It will generate a csv file (artist, title) with no duplications across charts and entries from the previous run.

Currently support table styles from following music charts:
- [billboard](https://www.billboard.com/charts/hot-100)
- [officialcharts](https://www.officialcharts.com/charts/singles-chart/)
- [euro200](https://euro200.net/)
- [tophit](https://tophit.ru/ru/chart/airplay_youtube/weekly/current/rus/new)
- [hitlisten](http://hitlisten.nu/default.asp?list=t40)
- [dutchcharts](https://dutchcharts.nl/weekchart.asp?cat=s)
- [acharts](https://acharts.co/france_singles_top_100)
- [ariacharts](https://www.ariacharts.com.au/charts/singles-chart)
- [mediaforest](http://www.mediaforest.ro/weeklycharts/HistoryWeeklyCharts.aspx)

## Installation
Clone this repository, install the packages in the requirement.txt, and google chrome.

## How to use?
- git clone and cd to repo.
- `cd RecordChartScrapper`
- Add/Remove chart info in charts.py
- run `python app.py`
- A csv file will be generated with a date.

## Contribute
Feel free to add more chart sources with the corresponding scraper method.
- Add your class base on sites/Base.py
- Add the corresponding information in charts.py 
- Could use help for http://www.radiomirchi.com
## Credits
Empty for now.

## License
See the license file.
