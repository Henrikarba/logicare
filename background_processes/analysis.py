import datetime
import math
import time
from datetime import timedelta

import pandas as pd


def read_file():
    df = pd.read_csv('data/tracking_data.csv')
    df["time"] = pd.to_datetime(df['time'] * 10 ** 9)

    l = len(df)
    df = df.drop_duplicates(['time', 'event_type'])
    # print(f'dropped {l - len(df)} duplicates')
    return df


def get_trajectories(df):
    rows = df.to_dict('records')
    trajectory_i = -1
    _rows = rows.copy()
    filtered_trajectories = []
    trajectory_begin = None
    for i, row in enumerate(rows):
        _rows[i]['trajectory'] = trajectory_i
        row['time'] = row['time'].to_pydatetime()

        if not trajectory_begin:  # first record of trajectory
            trajectory_begin = row['time']
        if row['event_type'] != 'move':  # click / scroll
            if timedelta(seconds=1) < row['time'] - trajectory_begin < timedelta(seconds=10):
                filtered_trajectories.append(trajectory_i)
            trajectory_i += 1
            trajectory_begin = None

    # print(f"found {len(filtered_trajectories)} good trajectories")

    rows = _rows
    _rows = []
    trajectory_i = 0
    prev = -1
    for row in rows:
        if row['trajectory'] in filtered_trajectories:
            if prev != row['trajectory']:
                prev = row['trajectory']
                trajectory_i += 1

            row['trajectory'] = trajectory_i
            _rows.append(row)

    rows = _rows

    trajectory_i = 0
    i = 0

    trajectories = []

    while i < len(rows):
        i0 = i
        i += 1  # to enable computations on i-1
        avg_speed = 0
        prev_time = rows[i0]['time']
        points_x = [rows[i0]['x']]
        points_y = [rows[i0]['y']]

        while i < len(rows) and rows[i]['event_type'] == 'move':  # rows[i]['trajectory'] == trajectory_i and
            avg_speed += math.sqrt((rows[i]['x'] - rows[i - 1]['x']) ** 2 + (rows[i]['y'] - rows[i - 1]['y']) ** 2) \
                         / (rows[i]['time'] - rows[i - 1]['time']).microseconds * 10 ** 6

            timepoint = prev_time + timedelta(milliseconds=300)
            while rows[i]['time'] >= timepoint:
                coef = (timepoint - rows[i - 1]['time']) / (rows[i]['time'] - rows[i - 1]['time'])
                points_x.append(rows[i - 1]['x'] + coef * (rows[i]['x'] - rows[i - 1]['x']))
                points_y.append(rows[i - 1]['y'] + coef * (rows[i]['y'] - rows[i - 1]['y']))
                prev_time = timepoint
                timepoint = prev_time + timedelta(milliseconds=300)

            i += 1

        eqdir = []
        for j in range(1, len(points_x) - 1):
            eqdir.append(int((points_x[j] - points_x[j - 1] > 0) == (points_x[j + 1] - points_x[j] > 0) \
                             and (points_y[j] - points_y[j - 1] > 0) == (points_y[j + 1] - points_y[j] > 0)))

        if eqdir:  # otherwise e.g. the movement itself was short, then a small pause and a click
            accuracy = sum(eqdir) / len(eqdir)

            n_events = i - i0
            avg_speed = avg_speed / n_events
            trajectories.append({'id': trajectory_i,
                                 'start': rows[i0]['time'],
                                 'end': rows[i]['time'],
                                 'speed': avg_speed,
                                 'accuracy': accuracy})

        i += 1  # account for click/scroll event in the end of trajectory
        trajectory_i += 1

    df = pd.DataFrame(trajectories)
    df['stress'] = - df['speed'] * df['accuracy'] + 3000
    return df


if __name__ == '__main__':
    # last_nudge_time = datetime.datetime(year=1970, month=1, day=1)
    while True:
        df = read_file()
        df = get_trajectories(df)
            
        try:
            dfcam = pd.read_csv('data/webcam_data.csv')
            dfcam["time"] = pd.to_datetime(df['time'] * 10 ** 9)
            fatigue_avg = dfcam.groupby(pd.Grouper(key='delta', freq='60S')).mean()['fatigue'].rolling(10, min_periods=3).mean()
            print(fatigue_avg)
            if fatigue_avg > 0.5:
                print('nudge')
        except:
            pass
        time_s = df.groupby(pd.Grouper(key='start', freq='60S')).mean()['stress'].rolling(10, min_periods=3).mean()
        last = time_s.iloc[-3:].to_list()
        if last[0] < last[1] < last[2]:
            print('issue nudge')


        time.sleep(60)



