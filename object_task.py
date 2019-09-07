import boto3
from PIL import Image, ImageDraw

client = boto3.client('rekognition')

bucket = 'aneekm-bucket'
refFile = 'ref_pic.jpg'
flipFlopRightFile = 'flip_flop_right.jpg'
shoeLeftFile = 'shoe_left.jpg'

def check_task(task, tgt):
    print('--- Task Starting ---')

    foundObj = False
    foundPerson = False

    response = client.detect_labels(
        Image={'S3Object':{'Bucket':bucket,'Name':tgt}},
        MaxLabels=10)

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

task1 = {'Id':1, 'ObjectLabel':'Shoe', 'ObjectQuality':'left'}
task2 = {'Id':2, 'ObjectLabel':'Flip-Flop', 'ObjectQuality':'exist'}

print("Task 1", check_task(task1, shoeLeftFile))
print("Task 2", check_task(task2, flipFlopRightFile))