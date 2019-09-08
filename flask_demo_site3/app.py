import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, Response, redirect, url_for
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
import json, boto3, base64, requests, random, string

auth = BotoAWSRequestsAuth(aws_host='http://api.strikeapoze.tech',
					aws_region='us-east-1',
					aws_service='execute-api')

username = None
prompt = None
taskID = None
objectType = None
quality = None
photoID = None
error_reason = None

# Create an S3 client
s3 = boto3.client('s3')

filename = 'file.txt'
bucket_name = 'my-bucket'

app = Flask(__name__)

def randomString(stringLength=10):
	letters = string.ascii_lowercase
	numbers = string.digits
	pool = letters + numbers
	return ''.join(random.choice(pool) for i in range(stringLength))

@app.route("/")
def index():
    global username, prompt
    username = None
    prompt = None
    taskID = None
    objectType = None
    quality = None
    photoID = None
    error_reason = None
    return render_template('index.html')

@app.route("/upload")
def upload():
	return render_template('upload.html')

@app.route("/success")
def success():
	global username, prompt
	username = None
	prompt = None
	return render_template('success.html')


@app.route("/failure")
def failure():
	return render_template('failure.html')


@app.route("/login", methods=["GET", "POST"])
def login():
	global username, prompt, taskID, photoID
	username = request.form.get("username")
	print(username)
	if checkUsername(username):
		taskID, objectType, quality = getTaskInfo()
		if (quality == "exist"):
			prompt = 'a picture of you holding a %s' % (objectType.lower())
		else:
			prompt = 'a picture of you holding a %s on the %s side of your face' % (objectType.lower(), quality.lower())
		photoID = randomString()
		return render_template('authenticate.html', prompt=prompt, photoID=photoID)
	return render_template('login.html')

@app.route("/authenticate/", methods=["GET", "POST"])
def authenticate():
	return render_template('authenticate.html')
	# if twoFactorAuthenticate(username):
	#     return render_template('success.html')
	# return render_template('login.html')

@app.route("/confirm/", methods=["GET", "POST"])
def confirm():
	global auth, username, taskID, photoID
	if (photoID == None): # OR OTHER FAILURE CASE
		return redirect(url_for('login'))
	print(taskID, username, photoID + '.png')

	body = {
		'taskId': taskID,
		'username': username,
		'livePicPath': photoID + '.png',
	}

	headers = {'Content-Type': 'application/json'}
	response = requests.post(
		'https://api.strikeapoze.tech/check-task',
		auth=auth, headers=headers, json=body)

	confirmed = json.loads(response.text)

	if (confirmed['res']):
		photoID = None
		return render_template('success.html')
	else:
		error_reason = confirmed['reason']
		return render_template('failure.html', rsn=error_reason)

@app.route('/task_refresh')
def task_refresh():
	# refreshTaskInfo()
	return("Hello")


def checkUsername(username):
	users = ["conlonn@andrew.cmu.edu", 'aneek@cmu.edu', 'eyluo@andrew.cmu.edu', 'manny@cmu.edu']
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

def refreshTaskInfo():
	global taskID, objectType, quality
	taskID, objectType, quality = getTaskInfo()


def getTaskInfo(): #TO-DO? Mostly done?
	global auth
	rawResponse = requests.get(
		'https://api.strikeapoze.tech/get-task',
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
