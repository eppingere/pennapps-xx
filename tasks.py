
import task_checker
import blink_things

def check_face(client, img1, img2):
    face_similarity_threshold = 95
    response=client.compare_faces(SimilarityThreshold=face_similarity_threshold,
                                  SourceImage={'Bytes': img1},
                                  TargetImage={'Bytes': img2})

    return len(response['FaceMatches']) == 1


def always_true(client, task, img_path):
    return True


def static_object(client, task, tgt):
    print('--- Static Object Task Starting ---')

    foundObj = False
    foundPerson = False

    #response = client.detect_labels(
    #    Image={'S3Object':{'Bucket':bucket,'Name':tgt}},
    #   MaxLabels=10)

    response = client.detect_labels(
        Image={'Bytes': tgt},
        MaxLabels=20
    )

    for label in response['Labels']:

        print ("Label: " + label['Name'])
        print ("Confidence: " + str(label['Confidence']))
        print ("Instances:", len(label['Instances']))
        print('-----------')
        print()

        if label['Name'] == task['ObjectLabel']:
            foundObj = True
            if len(label['Instances']) > 0:
                objLeft = label['Instances'][0]['BoundingBox']['Left']
                objRight = objLeft + label['Instances'][0]['BoundingBox']['Width']
        elif label['Name'] == 'Person':
            foundPerson = True
            if len(label['Instances']) > 0:
                personLeft = label['Instances'][0]['BoundingBox']['Left']
                personRight = personLeft + label['Instances'][0]['BoundingBox']['Width']

    if foundObj and foundPerson:
        if task['ObjectQuality'] == 'left':
            return objLeft < personLeft
        elif task['ObjectQuality'] == 'right':
            return objRight > personRight
        elif task['ObjectQuality'] == 'exist':
            return True
    else:
        return False

task_dict = {
    0 : always_true,
    1 : static_object,
    2 : static_object,
    3 : static_object,
}

task_arg_dict = {
    0 : {},
    1 : {'Id':1, 'ObjectLabel':'Shoe', 'ObjectQuality':'left'},
    2 : {'Id':2, 'ObjectLabel':'Flip-Flop', 'ObjectQuality':'exist'},
    3 : {'Id':3, 'ObjectLabel':'Cup', 'ObjectQuality':'exist'},
    4 : {'Id':3, 'ObjectLabel':'Beverage', 'ObjectQuality':'exist'},

}

numTasks = len(task_dict)    # always_true should be ignored and always be at index 0


if __name__ == '__main__':
    img0_path='img/face1.jpg'
    img1_path='img/water-bottle.jpg'

    img0=open(img0_path,'rb')
    img1=open(img1_path,'rb')

    print("result:", blink_things.live_check_task(3, img0, [img1]))

    img0.close()
    img1.close()
