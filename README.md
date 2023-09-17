![img.png](static/img.png)
# LogiCare

By Henri, Ilia, Lune and Jiayao at [HackZurich23](https://hackzurich.com/)
for Logitech challenge


## Background processes

1. **tracking.py**: tracks mouse movements, continuously writes them into a csv.
2. **blink_yawn_detection.py**: taps into web camera feed, recognizes the face, eyes, blinking and yawning.
3. **analysis.py**: combines results from first two, uses rules and formulas to decide whether to issue a nudge or not.
4. **gui/app.py**: frontend for data visualization, uses Dash.

## Data

* We provide two dumps of data to play with (Ilia's, almost a day of mouse tracking; Henri's, a few hours)
* Raw datapoints are sometimes as frequent as 100 times per second, but there are gaps in data - those are times when the person didn't use the laptop. 
* In analysis.ipynb you can find a notebook with analysis of that data, with some graphs. Trajectories are computed from raw data to better grasp a purposeful movement of a mouse; average speed and accuracy are measured ([see Banholzer et al., 2021](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8052599/))

## Limitations

* There are known issues with mouse tracking on Macs. Meaningful insights will only be produced after around 30 minutes of data.
* Data visualization part still contains mock data, even though real data is accessible. If one so desires, it is possible to modify gui/app.py in order to visualize findings.

### How to run?
* `pip install requirements.txt`
* `python app.py`
  * this command also triggers run of 4 background processes, which you can also run individually, if you wish.