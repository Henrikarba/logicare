import cv2
import dlib  # for face and landmark detection
import imutils
from scipy.spatial import distance as dist
from imutils import face_utils
from utils import *
import time
import code

cam = cv2.VideoCapture(0)
# cam.set(cv2.CAP_PROP_FPS, 20)

# Variables
blink_thresh = 0.38
yawn_thr = 1
succ_frame = 2
count_frame = 0

# Eye landmarks
(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']
(mouth_start, mouth_end) = face_utils.FACIAL_LANDMARKS_IDXS['inner_mouth']

# face detection
# detector = dlib.cnn_face_detection_model_v1('mmod_human_face_detector.dat')
detector = dlib.get_frontal_face_detector()
landmark_predict = dlib.shape_predictor(
    'shape_predictor_68_face_landmarks.dat')

if cam.isOpened():  # try to get the first frame
    res, image = cam.read()
else:
    res = False
total_blinks = 0
total_yawn = 0
elapsed_time = 0
last_yawn = time.time() - 10
per_minute_blink = []
per_minute_yawn = []
blink_timestamps = []
yawn_timestamps = []
fatigue_level = 0
# not_blinked = True
while res:
    if (time.time() - last_yawn) > 5:
        already_yawned = False
    if elapsed_time >= 60:
        # print(1/total_blinks, total_yawn/5)
        blink_callback(total_blinks)
        yawn_callback(total_yawn)
        fatigue_callback(total_blinks, total_yawn)
        print("wrote callbacks")
        per_minute_blink.append(total_blinks)
        per_minute_yawn.append(total_yawn)
        # print("blinks ", per_minute_blink)
        # print("yawns ", per_minute_yawn)
        total_blinks = 0
        total_yawn = 0
        elapsed_time = 0
    image = imutils.resize(image, width=640)
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    start_time = time.time()
    faces = detector(img_gray)
    # code.interact(local=dict(globals(), **locals()))
    # exit()
    # for face in faces:
    if len(faces) > 0:
        shape = landmark_predict(img_gray, faces[0])
        # visualize landmarks
        for n in range(0, 68):
            x = shape.part(n).x
            y = shape.part(n).y
            cv2.circle(image, (x, y), 1, (255, 155, 0), -1)
        shape = face_utils.shape_to_np(shape)
        #  eye aspect ratio
        lefteye = shape[L_start: L_end]
        righteye = shape[R_start:R_end]
        mouth = shape[mouth_start:mouth_end]
        left_EAR = calculate_EAR(lefteye)
        right_EAR = calculate_EAR(righteye)
        MAR = calculate_MAR(mouth)
        avg = (left_EAR + right_EAR) / 2
        # print(avg)
        if avg < blink_thresh:
            count_frame += 1  # incrementing the frame count
        if count_frame >= succ_frame:
            total_blinks += 1
            count_frame = 0
        if MAR > yawn_thr and not already_yawned:
            total_yawn += 1
            yawn_timestamps.append(time.time())
            already_yawned = True
            last_yawn = time.time()
        
        
        text = 'Blinks: ' + str(total_blinks) + " Yawns: " + str(total_yawn)
        if total_blinks > 0:
            text += " Fatigue: %.2f" % fatigue_level
        image = cv2.putText(
            img=image,
            text=text,
            org=(25, 25),
            fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=0.7,
            color=(225, 246, 55),
            thickness=2
        )
    cv2.imshow("cam", image)
    if total_blinks==0:
        fatigue_level = total_yawn/5 
    else:
        fatigue_level =  (total_yawn/5) + (1 / total_blinks)
        # print(1/total_blinks)
    # print(fatigue_level)
    # fatigue_level = (curr_fatigue + fatigue_level) / 2
    # print(curr_fatigue)
    # print("fatigue ", fatigue_level)
    # if fatigue_level > 0.7:
        # print("break")
    res, image = cam.read()
    elapsed_time += time.time() - start_time
    key = cv2.waitKey(20)
    if key == 27:  # exit on ESC
        break
cv2.destroyAllWindows()
cam.release()
