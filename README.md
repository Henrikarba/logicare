![img.png](static/img.png)
# LogiCare

By Henri, Ilia, Lune and Jiayao at [HackZurich23](https://hackzurich.com/)
for Logitech


## User status detection

* what user status to detect? concentration, fatigue
* to use webcam / keyboard / mouse
* decision logic of when to generate nudge (output from the user status detection module)

## Limitations

* There are known issues with mouse tracking on Macs. Meaningful insights will only be produced after around 30 minutes of data.

### How to run?
* `pip install requirements.txt`
* `python app.py`