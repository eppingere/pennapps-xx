import boto3
import json
import blink_things

from tasks import *

client = boto3.client('rekognition')

def check_task (task_id, refPic, livePics):
    print('--- Authenticating ---')

    if not blink_things.user_blinked(livePics):
        return False

    task_checker = task_dict[task_id]

    return task_checker(client, task_arg_dict[task_id], livePics, refPic)

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
        refPicPath = body['refPic']
        livePicsPath = body['livePics']

        auth = check_task(taskId, refPic, livePicsPath)

        return respond({'auth': auth}, None)
    else:
        return respond(None, {'message':'This endpoint only accepts POST requests!'})


if __name__ == "__main__":

    img0='ref_pic.jpg'
    img1='shoe_left.jpg'
    img2='flip_flop_right.jpg'
    img3='face1.jpg'

    print("always_true:", check_task(0, img0, 'face1.jpg'))
    print("shoe_left (should work):", check_task(1, img0, img1))
    print("flip_flop_right (should work):", check_task(2, img0, img2))
    print("shoe_left (should fail):", check_task(2, img3, img2))
    print("flip_flop_right (should fail):", check_task(2, img3, img2))
    print("ran!!")
