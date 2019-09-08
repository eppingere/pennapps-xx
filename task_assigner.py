import json
from random import choice
from tasks import *

def respond(resp, err):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(resp),
        'headers': {
            'Content-Type': 'application/json',
        },
    }

def lambda_handler(event, context):
    if event['httpMethod'] == 'GET':
        taskId = 0
        while taskId == 0:
            taskId = choice(list(task_arg_dict))

        return respond(
            {'description': task_arg_dict[taskId]},
            None)
    else:
        return respond(None,
            {'message':'This endpoint only accepts GET requests!'})
