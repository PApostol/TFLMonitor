from bs4 import BeautifulSoup
import requests, json


def get_service(soup, service):
    if service == 'good':
        temp = soup.find_all('div', class_='rainbow-list-link')
        info = [tag.text.split('\n\n\n\n') for tag in temp]
    elif service == 'bad':
        temp = soup.find_all('a', class_='rainbow-list-link')
        info = [tag.text.split('\n\n\n\n') for tag in temp if 'line-' in str(tag)]
    else:
        return

    res = {}
    for entry in info:
        line = entry[0].replace('\n', '').strip()
        status = entry[1].replace('\n', '').strip()
        res[line] = status

    return res


def get_tube_status():
    r = requests.get(r'https://tfl.gov.uk/tube-dlr-overground/status/')
    soup = BeautifulSoup(r.content, 'html.parser')

    good_service = get_service(soup, 'good')
    bad_service = get_service(soup, 'bad')

    return {**good_service, **bad_service}


def get_counter():
    return {'Good service': 0,
            'Minor delays': 0,
            'Severe delays': 0,
            'Part suspended': 0,
            'Part closure': 0,
            'Planned closure': 0}


def analyze_status(tracker, tube_status):
    for line, status in tube_status.items():
        counter = get_counter()
        for stat in counter:
            if stat in status:
                tracker[line][stat]+=1


def update_tracker(tracker):
    tube_status = get_tube_status()

    for line in tube_status:
        if line not in tracker:
            tracker[line] = get_counter()

    analyze_status(tracker, tube_status)


def print_tracker(tracker):
    for line, info in tracker.items():
        print(line)
        for status, counts in info.items():
            print(status + ': ' + str(counts))
        print('\n')


def save_tracker(tracker, filename):
    with open(filename+'.json', 'w') as f:
        json.dump(tracker, f)

