import matplotlib.pyplot as plt
import numpy as np
import json, glob, os


def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def add_two_trackers(tracker1, tracker2):
    ans = {}
    for line1, info1 in tracker1.items():
        info2 = tracker2.get(line1)

        temp = {}
        for status1, count1 in info1.items():
            count2 = info2.get(status1)
            temp[status1] = count1 + count2

        ans[line1] = temp
    return ans


def add_all_trackers():
    output_dir = os.path.dirname(os.getcwd()) + '/output/'
    full_data = {}
    first = True

    for file in glob.glob(output_dir + '*.json'):
        data = load_json(file)

        if first:
            full_data = data
            first = False
        else:
            full_data = add_two_trackers(data, full_data)
    return normalize_counts(full_data)


def normalize_counts(data):
    for line, info in data.items():
        total_counts = 0

        for status, count in info.items():
            total_counts += count

        for status in info:
            info[status]/=total_counts
    return data


def plot_all_trackers(start_date='?', end_date='?', grid=False):
    full_data = add_all_trackers()
    lines = [line.replace(' ', '\n') for line in full_data]
    statuses = [status for status in next(iter(full_data.values()))]

    status_counts = []
    for status in statuses:
        counter = []
        for line, info in full_data.items():
            counter.append(info.get(status)*100)

        status_counts.append(counter)

    fig, ax = plt.subplots()
    ind = np.arange(len(lines))
    width = 0.1

    p1 = ax.bar(ind-width*2, status_counts[0], width)
    p2 = ax.bar(ind-width, status_counts[1], width)
    p3 = ax.bar(ind, status_counts[2], width)
    p4 = ax.bar(ind+width, status_counts[3], width)
    p5 = ax.bar(ind+width*2, status_counts[4], width)
    p6 = ax.bar(ind+width*3, status_counts[5], width)

    ax.set_title('Tube Service between {0} and {1}'.format(start_date, end_date))
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(lines)

    ax.legend((p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]), statuses, bbox_to_anchor=(1.0, 1.0), fancybox=True, shadow=True)
    ax.autoscale_view()

    plt.ylabel('Percentage %')
    if grid:
        plt.grid()

    plt.show()