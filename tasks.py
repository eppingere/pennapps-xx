bucket = 'aneekm-bucket'

def check_face_static(client, img1, img2):
    face_similarity_threshold = 95
    response=client.compare_faces(SimilarityThreshold=face_similarity_threshold,
                                  SourceImage={'S3Object':{'Bucket':bucket,'Name':img1}},
                                  TargetImage={'S3Object':{'Bucket':bucket,'Name':img2}})

    return len(response['FaceMatches']) == 1


def always_true(client, task, img1, img2):
    return True


def static_object(client, task, tgt, ref):
    # print('--- Static Object Task Starting ---')

    if not check_face_static(client, ref, tgt):
        return False

    # print('--- Confirmed Face ---')

    foundObj = False
    foundPerson = False
    objLeft, objRight, personLeft, personRight = 0, 0, 0, 0

    response = client.detect_labels(
        Image={'S3Object':{'Bucket':bucket,'Name':tgt}},
        MaxLabels=20)

    for label in response['Labels']:

        '''print ("Label: " + label['Name'])
        print ("Confidence: " + str(label['Confidence']))
        print ("Instances:", len(label['Instances']))
        print('-----------')
        print()'''

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
    4 : static_object,
    5 : static_object,
    6 : static_object,
    7 : static_object,
    8 : static_object,
}

task_arg_dict = {
    0 : {},
    1 : {'Id':1, 'ObjectLabel':'Shoe', 'ObjectQuality':'left'},
    2 : {'Id':2, 'ObjectLabel':'Flip-Flop', 'ObjectQuality':'exist'},
    3 : {'Id':3, 'ObjectLabel':'Cup', 'ObjectQuality':'exist'},
    4 : {'Id':4, 'ObjectLabel':'Beverage', 'ObjectQuality':'exist'},
    5 : {'Id':5, 'ObjectLabel':'Bottle', 'ObjectQuality':'exist'},
    6 : {'Id':6, 'ObjectLabel':'Finger', 'ObjectQuality':'exist'},
    7 : {'Id':7, 'ObjectLabel':'Shoe', 'ObjectQuality':'right'},
    8 : {'Id':8, 'ObjectLabel':'Bag', 'ObjectQuality':'exist'},
}

numTasks = len(task_dict)    # always_true should be ignored and always be at index 0
