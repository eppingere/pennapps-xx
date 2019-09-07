import boto3
import json

from tasks import *

client = boto3.client('rekognition')
local_run = False

def check_task (task_id, refPic, livePics):
    print('--- Authenticating ---')
    faces_matched = False

    for userPic in livePics:
        if local_run:
            refPic.seek(0)
            userPic.seek(0)
        if check_face(client, refPic, userPic):
            faces_matched = True

    print('--- Confirmed Face ---')

    if not faces_matched:
        return False

    task_checker = task_dict[task_id]

    for userPic in livePics:
        if local_run:
            userPic.seek(0)
        if task_checker(client, task_arg_dict[task_id], userPic):
            return True

    return False

def respond(auth, err):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(auth),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    if event['httpMethod'] == 'POST':
        body = json.loads(event['body'])
        taskId = body['taskId']
        refPic = body['refPic']
        livePics = body['livePics']

        auth = check_task(taskId, refPic, livePics)

        return respond({'auth': auth}, None)
    else: 
        return respond(None, {'message':'This endpoint only accepts POST requests!'})


if __name__ == "__main__":
    local_run = True

    img0_path='img/ref_pic.jpg'
    img1_path='img/shoe_left.jpg'
    img2_path='img/flip_flop_right.jpg'

    img0=open(img0_path,'rb')
    img1=open(img1_path,'rb')
    img2=open(img2_path,'rb')

    print("result:", check_task(0, img0, [img1]))
    print("result:", check_task(1, img0, [img1]))
    print("result:", check_task(2, img0, [img2]))

    print("ran!!")
