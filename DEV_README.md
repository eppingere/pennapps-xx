# Pennapps XX Project - Poze

## Important Files:
1. **tasks.py** holds the functions for checking images
    against Rekognition, and the dictionaries defining the possible
    tasks
2. **task_assigner.py** is the Lambda handler for the 
    assignTasksLambda function in AWS. It returns a random task ID
    and description taken from `tasks.py`.
3. **task_checker.py** is the Lambda handler for the checkTaskLambda
    function in AWS. It takes an ID, a reference picture, and a list
    of live pictures and calls the appropriate validation function 
    from `tasks.py` with that data. **Currently Broken!**

## Deployment
AWS Lambda requires a zip file package to upload Python code.

To deploy:
1. Create a zip file containing the relevant files from the above 
    section for each function (tasks.py and one of the handlers)
2. Use the following AWS CLI command or upload using the web UI:
    `aws lambda update-function-code --function-name <FUNCTION> --zip-file fileb://<ZIPFILE>`

## Testing 
Use Postman for testing (API Gateway requires AWS SigV4 signed 
requests).
