import cv2
import dlib  # for face and landmark detection
import imutils
from scipy.spatial import distance as dist
from imutils import face_utils

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