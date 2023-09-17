import cv2
import dlib  # for face and landmark detection
import imutils
from scipy.spatial import distance as dist
from imutils import face_utils
import os
import time

file_name = 'data/tracking_data.csv'
def blink_callback(blinks_per_min):
    if not os.path.isfile(file_name):
        columns = ['event_type', 'button', 'x', 'y', 'delta', 'time']
        with open(file_name, 'a') as f:
            f.write(','.join(columns))
            f.write('\n')
    data = ["blink", "", "", "", str(blinks_per_min), str(time.time())]
    with open(file_name, 'a') as f:
        f.write(','.join(data))
        f.write('\n')

def yawn_callback(yawns_per_min):
    if not os.path.isfile(file_name):
        columns = ['event_type', 'button', 'x', 'y', 'delta', 'time']
        with open(file_name, 'a') as f:
            f.write(','.join(columns))
            f.write('\n')
    data = ["yawn", "", "", "", str(yawns_per_min), str(time.time())]
    with open(file_name, 'a') as f:
        f.write(','.join(data))
        f.write('\n')

# defining a function to calculate the EAR
def calculate_EAR(eye):
  
    # calculate the vertical distances
    y1 = dist.euclidean(eye[1], eye[5])
    y2 = dist.euclidean(eye[2], eye[4])
  
    # calculate the horizontal distance
    x1 = dist.euclidean(eye[0], eye[3])
  
    # calculate the EAR
    EAR = (y1+y2) / x1
    return EAR

# calculate mouth aspect ratio
def  calculate_MAR(inner_mouth):
    y1 = dist.euclidean(inner_mouth[1], inner_mouth[7])
    y2 = dist.euclidean(inner_mouth[3], inner_mouth[5])
    x1 = dist.euclidean(inner_mouth[0], inner_mouth[4])
    return (y1+y2) / x1