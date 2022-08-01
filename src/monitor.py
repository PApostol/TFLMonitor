"""
Main file for monitoring
"""
import argparse
import datetime
import glob
import logging
import os
import threading
import time

from plotting import plot_all_trackers
from scraping import save_tracker, update_tracker


class PlotThread(threading.Thread):
    def __init__(self, name, source_path, interval):
        threading.Thread.__init__(self)
        self.name = name.lower()
        self.source_path = source_path

        if interval < 60:
            interval = 60

        self.interval = interval
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def run(self):
        output_dir = os.path.dirname(os.getcwd()) + '/output/'
        pause = self.interval
        while True:
            # if no data, wait
            if not glob.glob(f'{output_dir}*.json'):
                time.sleep(pause)
            else:
                plot_all_trackers(self.source_path, self.name, pause=pause)


def get_date(incl_time: bool = False) -> str:
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d_%H-%M-%S') if incl_time else now.strftime('%Y-%m-%d')


def get_future_date(days: int) -> str:
    return (datetime.datetime.now() + datetime.timedelta(days=days)).strftime('%Y-%m-%d')


def main_scrape(days: float, interval: float, plot: str) -> None:
    start_date = get_date()
    end_date = get_future_date(int(days))

    output_dir = os.path.dirname(os.getcwd()) + '/output/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    today = start_date
    tracker = {}

    if plot is not None:
        plotting = PlotThread(plot, output_dir, interval)
        plotting.start()

    while today != end_date:
        update_tracker(tracker)
        now = get_date(incl_time=True)

        logging.info(f'Tracker updated on {now}')
        save_tracker(tracker, output_dir + now)

        time.sleep(float(interval) * 3600)
        today = get_date()

    if 'plotting' in locals():
        plotting.stop()


def cli_parser():
    parser = argparse.ArgumentParser(description='Transport for London Monitor')
    parser.add_argument('-d', '--days', help='Number of days to keep monitoring', type=float, required=False, default=1)
    parser.add_argument('-i', '--interval', help='Time interval in hours to update tracker', type=float, required=False, default=1)
    parser.add_argument('-p', '--plot', help='Plotting by "line" or "day"', type=str, required=False, default=None)
    return parser.parse_args()


if __name__ == '__main__':
    try:
        args = cli_parser()
        main_scrape(args.days, args.interval, args.plot)
    except Exception as err:
        raise
