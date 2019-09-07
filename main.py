import boto3

task_dict = dict()


def check_task(task_id, ref_pic, user_pics):

    if !user_blinked(user_pics):
        return false

    faces_matched = False

    for user_pic in user_pics:
        if same_face(ref_pic, user_pic):
            faces_matched = true
            continue

    if !faces_matched:
        return false


if __name__ == "__main__":

    # Replace sourceFile and targetFile with the image files you want to compare.
    sourceFile='img/face1.jpg'
    targetFile='img/face2.jpg'
    client=boto3.client('rekognition')

    imageSource=open(sourceFile,'rb')
    imageTarget=open(targetFile,'rb')

    response=client.compare_faces(SimilarityThreshold=70,
                                  SourceImage={'Bytes': imageSource.read()},
                                  TargetImage={'Bytes': imageTarget.read()})

    for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        confidence = str(faceMatch['Face']['Confidence'])
        print('The face at ' +
               str(position['Left']) + ' ' +
               str(position['Top']) +
               ' matches with ' + confidence + '% confidence')

    imageSource.close()
    imageTarget.close()
