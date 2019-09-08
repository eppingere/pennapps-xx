# Poze
Strike a Poze! An API for Private and Secure Identity Verification

Proudly built by [Aneek Mukherjee](https://aneekm.com), [Conlon Novak](https://conlonnovak.com), [Emmanuel Eppinger](https://eppi.ng), and [Eugene Luo](https://eyluo.github.io)


## Inspiration
An increasingly common problem for sites is dealing with fake users, users impersonating other users, and enforcement of best security practices with users. This problem is so severe that in [2018 Q4, Facebook identified 118 million impersonated accounts](https://www.nytimes.com/2019/01/30/technology/facebook-fake-accounts.html). Facebook's solution was to [ask users to upload photos of government issued IDs](https://kmph.com/news/local/facebook-is-asking-people-to-submit-their-ids-to-prove-their-accounts-are-real). However, this is an imperfect solution. Firstly, government IDs are quite easy to fake in real life, let alone in an image. Secondly, users may be understandably worried uploading images of personally identifiable documents onto the Internet. Our goal was to create a method to verify the identities of users without requiring any personally identifiable documents. 

## What It Does
Poze is a 2-factor authentication API designed to turn the stressful activity of account recovery and identity verification into a small, fun activity. The API works by asking users to "strike a Poze", that is, to do simple tasks on camera and uses Computer Vision to verify that they are accomplishing the task as specified and verifying that the person on camera is the correct owner of an account. For example, [if a scammer were to fake their identity on Facebook by using pictures of existing users](https://www.nytimes.com/2019/07/28/technology/facebook-military-scam.html), Facebook could provide both accounts the opportunity to confirm their identity by striking a Poze. The logic behind this verification process is that it is extremely unlikely that the average person has a picture of them online with a shoe on their head. Thus, when given an image of the user, Poze verifies that the person accomplishing their Poze in the video or image is the person they claim to be.

## How to Use Poze
Poze's API is designed for simple and easy yet effective use. To verify the identiy of a user, all you need is:

1. A photo of the user. You can get this before starting to call our API in each verification or you could pull this from data that the user has already provided.
2. Call our `api.strikeapoze.tech/get-task`, which will provide a Poze to ask the user to complete and a task ID.
3. Record a picture/video of the user accomplishing the task.
4. Send the recording to our `api.strikeapoze.tech/check-task` API.
5. Receive a `bool` representing whether or not the user has been verified

A complete definition of our API can be found in our [Swaggerdocs](http://eppi.ng/pennapps-xx/swagger/)

An example of how to use the Poze API is in our [demo](https://github.com/eppingere/pennapps-xx/tree/master/flask_demo_site3). 


## How We Built It
The core of Poze is [Amazon Rekognition](https://aws.amazon.com/rekognition/), a facial recognition and object detection service that we utilize to compare new pictures against references to authenticate a user. We wanted a serverless back-end, so we could focus on API transactions and not managing infrastructure, so Poze’s backend uses API Gateway to provide the necessary endpoints, and [AWS Lambda](https://aws.amazon.com/lambda/) to do the computation and interface with Rekognition. We also utilize [AWS S3](https://aws.amazon.com/s3/) to store the image and video files provided by our users to authenticate themselves, and ensure that their data is deleted in a timely fashion to maintain their privacy.
Our front-end example, called `PrivacyBook`, demonstrates how a service could implement the Poze API for verification. Built on Flask, JavaScript, and HTML5, PrivacyBook prompts the user to take a photo in their poze, and will let the user into their account on success.

## Challenges We Ran Into
We ran into issues trying to build a complex computer vision application, trying to deploy that in an AWS serverless environment, all while trying to stay within the confines of the AWS free tier. 
Amazon Rekognition is capable of labeling a lot of different objects, but struggles to define their location in the image. Oftentimes, we identified objects’ existence in the image, but Rekognition could only tag the person in the image, not the bottle or shoe, for example.

## Accomplishments We're Proud of
We were really proud of how the demo turned out. We really like how cleanly it demonstrates the power and promise of our API. We think it really highlights the ideal use case.
We also are quite happy with the overall design of our API. We think that the API design has a lot of promise and wouldn’t require much change in terms of going into production. 

## What We Learned
We learned a lot about AWS. Only Aneek had used AWS before this so learning about all the powerful APIs that AWS offers. We got experience designing, building, and deploying a serverless API.

## What's Next for Poze
* AR/VR activities via an external app to better guard against deepfakes.
* More interactive tasks for users to record that would provide more robust CAPTCHA functionality
* Fully implement a 2FA protocol that would allow Poze to function as a 2FA API for sites to use
