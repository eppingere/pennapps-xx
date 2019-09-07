import boto3
from imutils.video import FileVideoStream
from imutils import face_utils
import numpy as np
import dlib
import cv2

from task.tasks import always_true, check_face, static_object

task_dict = {
    0 : always_true,
    1 : static_object,
    2 : static_object,
}

task_arg_dict = {
    0 : {},
    1 : {'Id':1, 'ObjectLabel':'Shoe', 'ObjectQuality':'exist'},
    2 : {'Id':2, 'ObjectLabel':'Flip-Flop', 'ObjectQuality':'exist'},
}

# blink detection constants
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3

print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("util/shape_predictor_68_face_landmarks.dat")
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


def live_check_task(task_id, ref_pic, user_pics):

    if not user_blinked(user_pics):
        return False

    faces_matched = False

    for user_pic in user_pics:
        if same_face(ref_pic, user_pic):
            faces_matched = True
            continue

    if not faces_matched:
        return False

    task_checker = task_dict[task_id]

    for user_pic in user_pics:
        if task_checker(user_pic):
            return True

    return False

def eye_aspect_ratio(eye):
	# compute the euclidean distances between the two sets of
	# vertical eye landmarks (x, y)-coordinates
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# compute the euclidean distance between the horizontal
	# eye landmark (x, y)-coordinates
	C = dist.euclidean(eye[0], eye[3])

	# compute the eye aspect ratio
	ear = (A + B) / (2.0 * C)

	# return the eye aspect ratio
	return ear

def user_blinked(user_pics):
    COUNTER = 0
    TOTAL = 0

    if len(user_pics) == 0:
        return False

    if len(user_pics) < 100:
        return True

    frame = cv2.imread(user_pics[0].name)
    height, width, layers = frame.shape

    video = cv2.VideoWriter("temp/temp.avi", 0, 1, (width,height))

    for user_pic in user_pics:
        video.write(cv2.imread(user_pic.name))

    cv2.destroyAllWindows()
    video.release()

    vs = FileVideoStream("temp/temp.avi").start()

    for _ in user_pics:

        if TOTAL != 0:
            return True

        try:
            frame = vs.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            rects = detector(gray, 0)

            for rect in rects:
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)

                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)

                ear = (leftEAR + rightEAR) / 2.0

                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)

                if ear < EYE_AR_THRESH:
                    COUNTER += 1
                else:
                    if COUNTER >= EYE_AR_CONSEC_FRAMES:
                        TOTAL += 1

                    COUNTER = 0

        except Exception as e:
            print(e)
            continue

    return TOTAL > 0

    for user_pic in user_pics:
        if check_face(ref_pic, user_pic):
            faces_matched = True

    if not faces_matched:
        return False

    task_checker = task_dict[task_id]

    for user_pic in user_pics:
        if task_checker(task_arg_dict[task_id], user_pic):
            return True

    return False

if __name__ == "__main__":

    img0_path='img/ref_pic.jpg'
    img1_path='img/shoe_left.jpg'
    img2_path='img/flip_flop_right.jpg'

    img0=open(img0_path,'rb')
    img1=open(img1_path,'rb')
    img2=open(img2_path,'rb')

    print("testing face matching:", check_task(0, img1, [img2]))

    img1.close()
    img2.close()

    blink_imgs = []
    vc = cv2.VideoCapture("img/test-blinking.mp4")
    more, img = vc.read()
    frame_num = 0
    while more:
        cv2.imwrite("temp/frame%d.jpg" % frame_num, img)
        img_buf_reader = open("temp/frame%d.jpg" % frame_num, 'rb')
        blink_imgs.append(img_buf_reader)
        img_buf_reader.close()

        frame_num += 1
        more, img = vc.read()

    print("testing blink detction:", user_blinked(blink_imgs))

    print("ran!!")
