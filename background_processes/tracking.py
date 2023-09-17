import os.path
import random
import time
import mouse

file_name = 'data/tracking_data.csv'
columns = ['event_type', 'button', 'x', 'y', 'delta', 'time']
if not os.path.isfile(file_name):
    with open(file_name, 'a') as f:
        f.write(','.join(columns))
        f.write('\n')


prev_stress = 0.5
def callback(event: mouse.ButtonEvent | mouse.WheelEvent | mouse.MoveEvent):
    data = []
    if isinstance(event, mouse.ButtonEvent):
        data = [event.event_type, event.button, '', '', '', event.time]
    elif isinstance(event, mouse.WheelEvent):
        data = ['scroll', '', '', '', event.delta, event.time]
    elif isinstance(event, mouse.MoveEvent):
        data = ['move', '', event.x, event.y, '', event.time]

    data = [str(i) for i in data]

    # d = dict(zip(columns, data))
    # global prev_stress
    # prev_stress += (random.randint(0, 20)-10) / 100
    # d['stress'] = prev_stress
    # print(d)

    with open(file_name, 'a') as f:
        f.write(','.join(data))
        f.write('\n')


mouse.hook(callback)
while True:
    time.sleep(1000000)
