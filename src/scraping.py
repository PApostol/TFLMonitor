"""
File for scraping information from the web
"""
import json
import logging
from typing import Dict, Optional

import requests
from bs4 import BeautifulSoup

MAIN_URL = 'https://tfl.gov.uk/tube-dlr-overground/status/'

def get_service(soup: BeautifulSoup, service: str) -> Optional[Dict[str, str]]:
    if service == 'good':
        temp = soup.find_all('div', class_='rainbow-list-link')
        info = [tag.text.split('\n\n\n\n') for tag in temp]
    elif service == 'bad':
        temp = soup.find_all('a', class_='rainbow-list-link')
        info = [tag.text.split('\n\n\n\n') for tag in temp if 'line-' in str(tag)]
    else:
        return

    res: Dict[str, str] = {}
    for entry in info:
        if len(entry) > 1:
            line = entry[0].replace('\n', '').strip()
            status = entry[1].replace('\n', '').strip()
            res[line] = status

    return res


def get_tube_status() -> Dict[str, str]:
    r = requests.get(MAIN_URL)
    soup = BeautifulSoup(r.content, 'html.parser')

    good_service = get_service(soup, 'good')
    bad_service = get_service(soup, 'bad')

    return {**good_service, **bad_service}


def get_counter() -> Dict[str, int]:
    return {
        'Good service': 0,
        'Minor delays': 0,
        'Severe delays': 0,
        'Part suspended': 0,
        'Part closure': 0,
        'Planned closure': 0,
        'Special service': 0,
    }


def analyze_status(tracker: Dict[str, Dict[str, int]], tube_status: Dict[str, str]) -> None:
    for line, status in tube_status.items():
        counter = get_counter()
        for stat in counter:
            if stat in status:
                tracker[line][stat] += 1


def update_tracker(tracker: Dict[str, Dict[str, int]]) -> None:
    tube_status = get_tube_status()

    for line in tube_status:
        if line not in tracker:
            tracker[line] = get_counter()

    analyze_status(tracker, tube_status)


def print_tracker(tracker: Dict[str, Dict[str, int]]) -> None:
    for line, info in tracker.items():
        logging.info(line)
        for status, counts in info.items():
            logging.info(f'{status}: {counts}')
        logging.info('\n')


def save_tracker(tracker: Dict[str, Dict[str, int]], filename: str) -> None:
    with open(f'{filename}.json', 'w') as f:
        json.dump(tracker, f)
