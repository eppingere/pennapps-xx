# pennapps-xx
Poze: Private and Secure Identity Verification

## Inspiration
An increasingly common problem for sites is dealing with fake users, users impersonating other users, and enforcement of best security practices with users. This problem is so severe that in 2018 Q4, Facebook recognized 118 Million impersonated accounts. Facebook's solution is to ask users to upload photos of government issued IDs. However, this is an imperfect solution. Firstly, government IDs are quite easy to fake in real life, let alone in an image. Secondly, users may be understandably worried uploading images of personally identifiable documents to Facebook and other sites. Our goal was to create a method to verify the identities of users without requiring any personally identifiable documents. 

## What it does
Poze is an API that asks users to do simple tasks on camera and uses Computer Vision to verify that they are accomplishing the task as specified and verifying that the person on camera is the correct owner of the account. When given an image of the user, Poze verifies that the person in the video or image is the person in the user's image, therefore verifying that the person in control of the account is the person in control of the likeness displayed on the account.

## How we built it
The core of Poze is [Amazon Rekognition](https://aws.amazon.com/rekognition/), a facial recognition and object detection service that we utilize to compare new pictures against references to authenticate a user. We wanted a serverless back-end, so we could focus on API transactions and not managing infrastructure, so Poze’s backend uses API Gateway to provide the necessary endpoints, and [AWS Lambda](https://aws.amazon.com/lambda/) to do the computation and interface with Rekognition. We also utilize [AWS S3](https://aws.amazon.com/s3/) to store the image and video files provided by our users to authenticate themselves, and ensure that their data is deleted in a timely fashion to maintain their privacy.
Our front-end 

## Challenges we ran into
We ran into issues trying to build a complex computer vision application, trying to deploy that in an AWS serverless environment, all while trying to stay within the confines of the AWS free tier. 
Amazon Rekognition is capable of labeling a lot of different objects, but struggles to define their location in the image. Oftentimes, we identified objects’ existence in the image, but Rekognition could only tag the person in the image, not the bottle or shoe, for example.

## Accomplishments that we're proud of
We were really proud of how the demo turned out. We really like how cleanly it demonstrates the power and promise of our API. We think it really highlights the ideal use case.
We also are quite happy with the overall design of our API. We think that the API design has a lot of promise and wouldn’t require much change in terms of going into production. 

## What we learned
We learned a lot about AWS. Only Aneek had used AWS before this so learning about all the powerful APIs that AWS offers. We got experience designing, building, and deploying a serverless API.

## What's next for Poze
* AR/VR activities via an external app improvements to better guard against deepfakes.
* More interactive tasks for users to record that would provide more robust CAPTCHA functionality
* Fully implement a 2FA protocol that would allow Poze to function as a 2FA API for sites to use
