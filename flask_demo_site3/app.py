import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, Response, redirect, url_for
from task_assigner import respond, lambda_handler
from tasks import *
import json

import boto3
# from boto3.dynamodb.conditions import Key, Attr
import json

import base64, requests
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth

auth = BotoAWSRequestsAuth(aws_host='htozj1y344.execute-api.us-east-1.amazonaws.com',
                    aws_region='us-east-1',
                    aws_service='execute-api')

user = None
prompt = None

# Create an S3 client
s3 = boto3.client('s3')

filename = 'file.txt'
bucket_name = 'my-bucket'

app = Flask(__name__)

# dynamodb= boto3.resource('dynamodb')
# insurers_table = dynamodb.Table('insurers')
# hospitals_table = dynamodb.Table('hospitals')
@app.route("/")
def index():
	global user, prompt
	user = None
	prompt = None
	return render_template('index.html')


@app.route("/success")
def success():
	global user, prompt
	user = None
	prompt = None
	return render_template('success.html')


@app.route("/login", methods=["GET", "POST"])
def login():
	global user, prompt
	username = request.form.get("username")
	print(username)
	if checkUsername(username):
		taskID, objectType, quality = getTaskInfo()
		if (quality == "exist"):
			prompt = 'a picture of you holding a %s' % (objectType.lower())
		else:
			prompt = 'a picture of you holding a %s on the %s side of your face' % (objectType.lower(), quality.lower())
		return render_template('authenticate.html', prompt=prompt)
	return render_template('login.html')

@app.route("/authenticate/", methods=["GET", "POST"])
def authenticate():
	return render_template('authenticate.html')
	# if twoFactorAuthenticate(user):
	# 	return render_template('success.html')
	# return render_template('login.html')

def checkUsername(username): 
	users = ["conlonn@andrew.cmu.edu", 'aneekm@andrew.cmu.edu',
    	'eyluo@andrew.cmu.edu', 'manny@cmu.edu']
	if username in users:
		return True
	else: 
		print("Username not in \"database.\"")
		return False

def twoFactorAuthenticate(username):
	#same face?
	#did they blink?
	taskID, objectType, quality = getTaskInfo()
	print(taskID, objectType, quality)
	# prompt = "Take a picture of yourself holding a %s in your %s hand" % ()
	# Prompt user to take photo on webcam
	# uploadPhotoS3(pic)
	# return checkTask(taskID, username, livePath)
	return True

def getTaskInfo(): #TO-DO? Mostly done?
	global auth
	rawResponse = requests.get(
        'https://htozj1y344.execute-api.us-east-1.amazonaws.com/default/get-task',
        auth=auth)

	if (rawResponse == None):
		return None, None, None

	responseJSON = json.loads(rawResponse.text)['description']

	return responseJSON['Id'], responseJSON['ObjectLabel'], responseJSON['ObjectQuality']

def uploadPhotoS3(pic): #TO-DO
	# Uploads the given file using a managed uploader, which will split up large
	# files automatically and upload parts in parallel.
	s3.upload_file(filename, bucket_name, filename)


def checkTask(): #TO-DO
	global auth
	response = requests.post(
        'https://htozj1y344.execute-api.us-east-1.amazonaws.com/default/get-task',
        auth=auth)

def registerNewUser(): #TO-DO
	#username
	#password
	#reference picture
	return None

#how are we adding new users to s3
