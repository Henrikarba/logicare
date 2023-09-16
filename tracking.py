import os.path
import time
import mouse

file_name = 'mouse_tracking_data.txt'
columns = ['event_type', 'button', 'x', 'y', 'delta', 'time']
if not os.path.isfile(file_name):
    with open(file_name, 'a') as f:
        f.write(','.join(columns))
        f.write('\n')


def callback(event: mouse.ButtonEvent | mouse.WheelEvent | mouse.MoveEvent):
    data = []
    if isinstance(event, mouse.ButtonEvent):
        data = [event.event_type, event.button, '', '', '', event.time]
    elif isinstance(event, mouse.WheelEvent):
        data = ['scroll', '', '', '', event.delta, event.time]
    elif isinstance(event, mouse.MoveEvent):
        data = ['move', '', event.x, event.y, '', event.time]

    data = [str(i) for i in data]

    with open(file_name, 'a') as f:
        f.write(','.join(data))
        f.write('\n')


mouse.hook(callback)
while True:
    time.sleep(1000000)
