from scraping import update_tracker, save_tracker
from plotting import plot_all_trackers
import time, os, datetime, argparse


def get_date(incl_time=False):
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d_%H-%M-%S') if incl_time else now.strftime('%Y-%m-%d')


def get_future_date(days):
    return (datetime.datetime.now() + datetime.timedelta(days=days)).strftime('%Y-%m-%d')


def main(days, interval):
    start_date = get_date()
    end_date = get_future_date(int(days))

    output_dir = os.path.dirname(os.getcwd()) + '/output/'
    today = start_date
    tracker = {}

    while today != end_date:
        update_tracker(tracker)
        now = get_date(incl_time=True)

        print('Tracker updated on ' + now)
        save_tracker(tracker, output_dir + now)

        time.sleep(float(interval)*3600)
        today = get_date()

    plot_all_trackers(start_date, end_date)


def cli_parser():
    parser = argparse.ArgumentParser(description='Transport for London Monitor')
    parser.add_argument('-d', '--days', help='Number of days to keep monitoring', required=False, default=1)
    parser.add_argument('-i', '--interval', help='Time interval in hours to update tracker', required=False, default=1)
    return parser.parse_args()


if __name__=='__main__':
    try:
        args = cli_parser()
        main(args.days, args.interval)
    except Exception as err:
        raise err
