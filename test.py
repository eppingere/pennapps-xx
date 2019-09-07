# python script to build the API request for Postman to send

import base64, json, requests
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth

with open('img/ref_pic.jpg','rb') as refPic, open('img/flip_flop_right.jpg','rb') as shoePic:
    body = {
        'taskId':2,
        'refPic':base64.b64encode(refPic.read()).decode('utf-8'),
        'livePics':[
            base64.b64encode(shoePic.read()).decode('utf-8')
        ]
    }

    auth = BotoAWSRequestsAuth(aws_host='htozj1y344.execute-api.us-east-1.amazonaws.com',
                        aws_region='us-east-1',
                        aws_service='execute-api')

    headers = {'Content-Type':'application/json'}
    response = requests.post(
        'https://htozj1y344.execute-api.us-east-1.amazonaws.com/default/check-task',
        auth=auth, headers=headers, json=body)

    print(response.text)