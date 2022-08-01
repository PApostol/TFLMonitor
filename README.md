## TFL Monitor

Monitors the status of all TFL underground and overground lines for a given time period and logging interval. Plots and updates figure according to specified interval.

Developed and tested on Ubuntu 20.04.
Works with:

* [Python](https://www.python.org/ "Python's Homepage") (3.7+)

Requirements:
- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [matplotlib](https://matplotlib.org/)

### Instructions for deployment
- Clone the repo `https://github.com/PApostol/TFLmonitor.git`.
- Usage: `python monitor.py [-h] [-d DAYS] [-i INTERVAL] [-p PLOT]`

    Defaults: DAYS=1, INTERVAL=1, PLOT=None

    Examples:
    
    `python monitor.py -d 7 -i 0.5 -p day` - run for 7 days, acquire data every 0.5 hour, plot results by day
    
    `python monitor.py -d 1 -i 2 -p line` - run for 1 day, acquire data every 2 hours, plot results by line
