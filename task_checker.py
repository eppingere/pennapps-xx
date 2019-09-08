import boto3
import json
#import blink_things

from tasks import *

client = boto3.client('rekognition')

def check_task (task_id, refPicPath, livePicsPath):
    # print('--- Authenticating ---')

    #if not blink_things.user_blinked(livePics):
     #   return False

    task_checker = task_dict[task_id]

    print("Running task checker:", task_arg_dict[task_id])

    return task_checker(client, task_arg_dict[task_id], livePicsPath, refPicPath)

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
        refPicPath = body['username'] + '.png'
        livePicsPath = body['livePicPath']

        print('Ref:',refPicPath,'Live:',livePicsPath)
        auth = check_task(taskId, refPicPath, livePicsPath)

        return respond(auth, None)
    else:
        return respond(None, {'message':'This endpoint only accepts POST requests!'})


if __name__ == "__main__":

    ref_aneek = 'aneek@cmu.edu.png'
    ref_manny = 'manny@cmu.edu.png'

    shoe_left='shoe_left.jpg'
    shoe_left_new='fa5nf6kxl6.png'
    shoe_right_new='q2j0llfu81.png'
    shoe_right = 'shoe_right.jpg'
    flip_flop_right='flip_flop_right.jpg'
    cup = 'cup.jpg'
    beverage = 'bev.jpg'
    bottle = 'bot.jpg'
    finger = 'finger.jpg'

    assert(check_task(0, ref_manny, 'face1.jpg')['res']) # always_true
    assert(check_task(1, ref_aneek, shoe_left_new)['res']) # shoe_left
    assert(check_task(2, ref_aneek, flip_flop_right)['res']) # flip_flop_right
    assert(not check_task(2, ref_manny, shoe_right_new)['res']) # shoe_left failure
    assert(not check_task(2, ref_manny, flip_flop_right)['res']) # flip_flop_right failure
    assert(check_task(3, ref_manny, cup)['res']) # cup
    assert(check_task(4, ref_manny, beverage)['res']) # beverage
    assert(check_task(5, ref_manny, bottle)['res']) # bottle
    assert(check_task(6, ref_manny, finger)['res']) # finger
    assert(check_task(7, ref_aneek, shoe_right_new)['res']) # shoe_right

    print("all tests passed!!")
