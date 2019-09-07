from flask import Flask, render_template, request, Response, redirect

# import boto3
# from boto3.dynamodb.conditions import Key, Attr
import json

#TO-DO:
# 1. Solve the error with 'WAIT' not being a valid field in the dynamodb
# 2. Make sure that we can change the wait times with the three that we showed
# 3. Stand the thing up in S3 
# 4. Fix the URL_FOR error that we keep getting: 


# Helper class to convert a DynamoDB item to JSON.
# class DecimalEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, decimal.Decimal):
#             if o % 1 > 0:
#                 return float(o)
#             else:
#                 return int(o)
#         return super(DecimalEncoder, self).default(o)


app = Flask(__name__)
# dynamodb= boto3.resource('dynamodb')
# insurers_table = dynamodb.Table('insurers')
# hospitals_table = dynamodb.Table('hospitals')

@app.route("/success")
def success(): 
	return render_template('welcome.html')


@app.route("/login", methods=["GET", "POST"])
def login():
	username = request.form.get("username")
	print(username)
	if checkusername(username):
		#THIS SHOULD BE WHERE WE CHECK WITH ARioWare---------------------------------------------------
		# response = hospitals_table.query(
  #  		KeyConditionExpression=Key('name').eq(username)
		# )
		# info = response['Items'][0]
		# print(info)
		# ##want to get address, phone number, wait time
		return render_template("2fa.html", username=username)
	return render_template('login.html')

@app.route("/2fa", methods=["GET", "POST"])
def twoFactor(username):
	if twoFactorAuthenticate(username):
		#THIS SHOULD BE WHERE WE CHECK WITH ARioWare---------------------------------------------------
		# response = hospitals_table.query(
  #  		KeyConditionExpression=Key('name').eq(username)
		# )
		# info = response['Items'][0]
		# print(info)
		# ##want to get address, phone number, wait time
		return render_template('welcome.html')
	return render_template('login.html')

def checkusername(username): 
	#username = request.form.get("username")
	if username in ["conlonn@andrew.cmu.edu", 'aneekm@andrew.cmu.edu','eyluo@andrew.cmu.edu','manny@cmu.edu']:
		return True
	else: 
		print("doesnt work")
		return False

def twoFactorAuthenticate(username):
	return True