import boto3

def always_true(img_path):
    return True

task_dict = {
    0 : always_true
}

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
