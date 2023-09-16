import cv2
import dlib  # for face and landmark detection
import imutils
from scipy.spatial import distance as dist
from imutils import face_utils
cam = cv2.VideoCapture(0)
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
  
# Variables
blink_thresh = 0.45
succ_frame = 2
count_frame = 0
  
# Eye landmarks
(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

# face detection
detector = dlib.get_frontal_face_detector()
landmark_predict = dlib.shape_predictor(
    'shape_predictor_68_face_landmarks.dat')

if cam.isOpened(): # try to get the first frame
    res, image = cam.read()
else:
    res = False
    print('nope')
total_blinks = 0

while res:
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(img_gray)
    for face in faces:
        shape = landmark_predict(img_gray, face)
        # visualize landmarks
        for n in range(0, 68):
            x = shape.part(n).x
            y = shape.part(n).y
            cv2.circle(image, (x, y), 4, (255, 0, 0), -1)
        shape = face_utils.shape_to_np(shape)
        lefteye = shape[L_start: L_end]
        righteye = shape[R_start:R_end]
        left_EAR = calculate_EAR(lefteye)
        right_EAR = calculate_EAR(righteye)
        avg = (left_EAR+right_EAR)/2
        if avg < blink_thresh:
            count_frame += 1  # incrementing the frame count

        if count_frame >= succ_frame:
            total_blinks += 1
            # image = cv2.putText(image, text, (30, 30),
                        # cv2.FONT_HERSHEY_DUPLEX, 1, (0, 200, 0), 1)
   
            count_frame = 0
    text = 'Blink Detected: ' + str(total_blinks)
    image = cv2.putText(
  img = image,
  text = text,
  org = (200, 200),
  fontFace = cv2.FONT_HERSHEY_DUPLEX,
  fontScale = 3.0,
  color = (125, 246, 55),
  thickness = 3
)
    cv2.imshow("cam",image)
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    res, image = cam.read()
    

cv2.destroyAllWindows()
cam.release()