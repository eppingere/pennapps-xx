from flask import Flask, render_template, request, Response, redirect, url_for

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

users = ["conlonn@andrew.cmu.edu", 'aneekm@andrew.cmu.edu','eyluo@andrew.cmu.edu','manny@cmu.edu']

# dynamodb= boto3.resource('dynamodb')
# insurers_table = dynamodb.Table('insurers')
# hospitals_table = dynamodb.Table('hospitals')
@app.route("/")
def index(): 
	user = None
	prompt = None
	return render_template('index.html')


@app.route("/success")
def success(): 
	user = None
	prompt = None
	return render_template('success.html')


@app.route("/login", methods=["GET", "POST"])
def login():
	username = request.form.get("username")
	print(username)
	if checkusername(username):
		user = username
		return redirect(url_for('authenticate'))
	return render_template('login.html')

@app.route("/authenticate/", methods=["GET", "POST"])
def authenticate():
	if twoFactorAuthenticate(user):
		return render_template('success.html')
	return render_template('login.html')

def checkusername(username): 
	if username in users:
		return True
	else: 
		print("Username not in \"database.\"")
		return False

def twoFactorAuthenticate(username):
	return True
	#same face?
	#did they blink?
	# task_id, obj_label, obj_qual = get_task()
	# upload_photo_s3(pic)
	# return check_task()

def get_task(): #TO-DO? Mostly done?
	response = requests.get(
        'https://htozj1y344.execute-api.us-east-1.amazonaws.com/default/get-task',
        auth=auth)

	print(response.text)
    #dictionary of ID, obj label, obj quality
    #build prompt and display it

def upload_photo_s3(pic): #TO-DO
	# Uploads the given file using a managed uploader, which will split up large
	# files automatically and upload parts in parallel.
	s3.upload_file(filename, bucket_name, filename)


def check_task(): #TO-DO
	response = requests.post(
        'https://htozj1y344.execute-api.us-east-1.amazonaws.com/default/get-task',
        auth=auth)

def register(): #TO-DO
	#username
	#password
	#reference picture
	return None

#how are we adding new users to s3