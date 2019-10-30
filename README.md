## TFL Monitor

Monitors the status of all TFL underground and overground lines for a given time period and logging interval. Plots findings on bar plot.

Developed and tested on Ubuntu 18.04.
Made with:

* [Python](https://www.python.org/ "Python's Homepage") (3.6 or newer)

Requirements:
- [requests](https://pypi.org/project/requests/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
- [matplotlib](https://matplotlib.org/)

### Instructions for deployment
- Clone the repo `https://github.com/PApostol/TFLmonitor.git`.
- Usage: `python3 src/main.py [-h] [-d DAYS] [-i INTERVAL]`.