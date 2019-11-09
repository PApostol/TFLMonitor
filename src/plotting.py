import matplotlib.pyplot as plt
import numpy as np
import json, glob, os, time, re, datetime, calendar, sys


def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def add_two_trackers(tracker1, tracker2):
    if tracker1 is None:
        return tracker2
    elif tracker2 is None:
        return tracker1
    elif (tracker1 is None) and (tracker2 is None):
        return

    ans = {}
    for line1, info1 in tracker1.items():
        info2 = tracker2.get(line1)

        temp = {}
        for status1, count1 in info1.items():
            count2 = info2.get(status1)
            temp[status1] = count1 + count2

        ans[line1] = temp
    return ans


def add_all_trackers_by_line(source_path):
    full_data = None
    timestamps = []

    for file in glob.glob(source_path + '*.json'):
        data = load_json(file)
        filename = file.replace('\\', r'/').split('/').pop()

        timestamps.append(filename.split('_').pop(0))
        full_data = add_two_trackers(data, full_data)

    timestamps.sort()
    return normalize_counts(full_data), timestamps[0], timestamps[-1]


def add_all_lines_by_day(full_data):
    res = {}
    for day, info in full_data.items():
        day_status = {}
        for status in info.values():
            for stat, count in status.items():
                if stat in day_status:
                    day_status[stat]+=count
                else:
                    day_status[stat]=count
        res[day]=day_status
    return res


def add_all_trackers_by_day(source_path):
    full_data = {'Monday': None,
                 'Tuesday': None,
                 'Wednesday': None,
                 'Thursday': None,
                 'Friday': None,
                 'Saturday': None,
                 'Sunday': None}

    timestamps = []
    for file in glob.glob(source_path + '*.json'):
        data = load_json(file)
        filename = file.replace('\\', r'/').split('/').pop()

        timestamps.append(filename.split('_').pop(0))
        match = re.search(r'\d{4}-\d{2}-\d{2}', filename)
        
        if not match.group():
            continue
        else:
            day = calendar.day_name[datetime.datetime.strptime(match.group(), '%Y-%m-%d').weekday()]

        full_data[day] = add_two_trackers(data, full_data[day])

    filtered_days = add_all_lines_by_day({key: val for key, val in full_data.items() if val is not None})
    timestamps.sort()

    return normalize_counts(filtered_days), timestamps[0], timestamps[-1]


def normalize_counts(data):
    for line, info in data.items():
        total_counts = 0

        for status, count in info.items():
            total_counts += count

        for status in info:
            info[status]/=total_counts
    return data


def plot_all_trackers(source_path, option, pause=0, grid=False):
    if 'line' in option:
        full_data, start_date, end_date = add_all_trackers_by_line(source_path)
    elif 'day' in option:
        full_data, start_date, end_date = add_all_trackers_by_day(source_path)
    else:
        print('Plotting option "{0}" not recognized!'.format(option))
        sys.exit(1)

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

    output_dir = os.path.dirname(os.getcwd()) + '/output/figures/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if start_date==end_date:
        ax.set_title('London TFL Service on {0}'.format(start_date))
        fig_name = output_dir + '{0}.pdf'.format(start_date)
    else:
        ax.set_title('London TFL Service between {0} and {1}'.format(start_date, end_date))
        fig_name = output_dir + '{0}_{1}.pdf'.format(start_date, end_date)

    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(lines)

    ax.legend((p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]), statuses, bbox_to_anchor=(1.0, 1.0), fancybox=True, shadow=True)
    ax.autoscale_view()

    plt.ylabel('Percentage of Time %')
    if grid:
        plt.grid()

    plt.savefig(fig_name)
    plt.ion()
    plt.show()
    plt.pause(0.001)
    time.sleep(pause)
    plt.close(fig)
