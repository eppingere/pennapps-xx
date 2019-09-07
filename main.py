import boto3
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2

def always_true(img_path):
    return True

task_dict = {
    0 : always_true
}

# blink detection constants
EYE_AR_THRESH = 0.3
EYE_AR_CONSEC_FRAMES = 3

print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("util/shape_predictor_68_face_landmarks.dat")
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


def check_task(task_id, ref_pic, user_pics):

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

def user_blinked(user_pics):
    COUNTER = 0
    TOTAL = 0

    if len(user_pics) == 0:
        return False

    frame = cv2.imread(user_pics[0].name)
    height, width, layers = frame.shape

    video = cv2.VideoWriter("temp.mp4", 0, 1, (width,height))

    for user_pic in user_pics:
        video.write(cv2.imread(user_pic.name))

    cv2.destroyAllWindows()
    video.release()

    vs = FileVideoStream("temp.mp4").start()

    for _ in user_pics:
        try:
            print("here")
            frame = vs.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            print("here")

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


    # return TOTAL > 0
    return True



def same_face(img1, img2):
    face_similarity_threshold = 95
    client=boto3.client('rekognition')
    response=client.compare_faces(SimilarityThreshold=face_similarity_threshold,
                                  SourceImage={'Bytes': img1.read()},
                                  TargetImage={'Bytes': img2.read()})

    return len(response['FaceMatches']) == 1


if __name__ == "__main__":

    img1_path='img/face1.jpg'
    img2_path='img/face2.jpg'

    img1=open(img1_path,'rb')
    img2=open(img2_path,'rb')

    print("result:", check_task(0, img1, [img2]))

    print("ran!!")
