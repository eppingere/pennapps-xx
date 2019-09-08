<p align="center">
  <img src="https://github.com/eppingere/pennapps-xx/raw/master/img/poze.png" width="454" />
</p>

# Poze
Strike a Poze! An API for Private and Secure and Fun Identity Verification

Proudly built by [Aneek Mukherjee](https://aneekm.com), [Conlon Novak](https://conlonnovak.com), [Emmanuel Eppinger](https://eppi.ng), and [Eugene Luo](https://eyluo.github.io).

## Inspiration
An increasingly common problem for sites is dealing with fake users, users impersonating other users, and enforcement of best security practices with users. This problem is so severe that in [2018 Q4, Facebook identified 118 million impersonated accounts](https://www.nytimes.com/2019/01/30/technology/facebook-fake-accounts.html). Facebook's solution was to [ask users to upload photos of government issued IDs](https://kmph.com/news/local/facebook-is-asking-people-to-submit-their-ids-to-prove-their-accounts-are-real). However, this is an imperfect solution. Firstly, government IDs are quite easy to fake in real life, let alone in an image. Secondly, users are understandably worried about uploading images of personally identifiable documents onto the Internet. **Our goal was to create a method of verifying the identities of users without requiring any personal documents and letting them have fun while doing so!**

## What It Poze?
Poze is a 2-factor authentication API designed to turn the stressful activity of account recovery and identity verification into a small, fun activity. 


First, what is 2-factor authentication([2FA](https://authy.com/what-is-2fa/))? Essentially, 2FA provides a _second factor_ in authenticating your identity, whether that be something you have, like a phone, something you know, like a special code, or, by taking advantage of new technologies like CV and ML, something you are, like **your face!**


Poze works by asking users to "strike a Poze" - to do small, silly tasks on camera. Using Computer Vision, Poze then verifies that the user is accomplishing the task as specified **and** verifying that the person on camera is the owner of an account. For example, [if a scammer were to fake their identity on Facebook by using pictures of existing users](https://www.nytimes.com/2019/07/28/technology/facebook-military-scam.html), Facebook could provide both accounts the opportunity to confirm their identity by striking a Poze. By providing a reasonable time limit on all parties, Facebook can verify the user whose picture is being used and identify scammers - because most people don't have easy-to-find pictures online of them with a shoe on the side of their head or a banana next to their face! Thus, Poze can provide security to users and companies by verifying that the person accomplishing their Poze is the person they claim to be.

## How to Use Poze
Poze's API is designed for simplicity and effectiveness. To verify the identtiy of a user, you will need the following.

1. A photo of the user. You can get this before starting to use our API in each verification or you could pull this from data that the user has already provided.
2. A call to the `api.strikeapoze.tech/get-task` API, which will provide a Poze to ask the user to complete and a task ID.
3. A picture/video of the user accomplishing the task.
4. A call to our `api.strikeapoze.tech/check-task` API, containing the picture or video of the user and the reference picture identifier. This call will return a `bool` representing whether or not the user has been verified, and a `string` with details when the authentication fails.

A complete definition of our API can be found in our [Swaggerdocs](http://eppi.ng/pennapps-xx/swagger/).

An example of how to use the Poze API is in our [demo](https://github.com/eppingere/pennapps-xx/tree/master/flask_demo_site3).


## How We Built It
The core of Poze is [Amazon Rekognition](https://aws.amazon.com/rekognition/), a facial recognition and object detection service that we utilize to compare new pictures against references to authenticate a user. We wanted a serverless back-end so that we could focus on API transactions and not managing infrastructure, so Poze’s backend uses API Gateway to provide the necessary endpoints, and [AWS Lambda](https://aws.amazon.com/lambda/) to do the computation and interface with Rekognition. We also utilize [AWS S3](https://aws.amazon.com/s3/) to store the image and video files provided by our users to authenticate themselves, and ensure that their data is deleted in a timely fashion to maintain their privacy.

Our front-end example, called `PrivacyBook`, demonstrates how a service could implement the Poze API for verification. Built on Flask, JavaScript, and HTML5, PrivacyBook prompts the user to take a photo in their poze, and will let the user into their account on success.

## Challenges We Ran Into
We ran into issues trying to build a complex computer vision application; our personal machines don't have the necessary power to extensively train new models. Deploying a CV application requires a lot of complex Python computation libraries, and trying to deploy that in an AWS serverless environment was quite difficult. For most of the weekend, we also needed to ensure we stayed within the bounds of the AWS Free tier while doing this. 

A big challenge we had to tackle was that Amazon Rekognition is capable of labeling a lot of different objects, but struggles to define their location in the image. Oftentimes, we identified objects’ existence in the image, but Rekognition could only tag the person in the image, not the bottle or toy, for example. Thus, some of our prompts are less specific than others - merely the presence of an object in the image rather than in a specific orientation. 

## Accomplishments We're Proud of
We are really proud of the simplicity of the design of our API. One of the most important things in developing a service like this is ease of use, and we think our API is very easy to use and to integrate with. We are also really excited about the current performance of the authentication after just a day and a half of development. We believe that the demo really cleanly demonstrates the power and promise of the service, and highlights the ideal use case. It also shows the potential for Poze to continue to expand and become more secure, more fun, and more random!

## What We Learned
One of the biggest learning experiences over the weekend was creating a service that was so tightly integrated with AWS. Only one team member, Aneek, had used AWS before this, so researching and taking advantage of the powerful services that AWS offers was a really new and exciting experience. We all got a lot of hands-on experience architecting, coding, and deploying a serverless API interfacing with multiple AWS services.

We also deployed a demo UI for Poze - PrivacyBook - that is built on Flask, JavaScript, and HTML5/CSS3. This was one of the most significant UI projects that we'd worked on, on top of the development of the back-end. We learned a lot about integrating JavaScript with Flask and intelligently designing the user experience so that we could our users could intuitively navigate through our UI.

## What's Next for Poze
* AR pozes via a mobile app experience to better guard against AI-generated pictures and videos
* More interactive tasks for users to record that would provide more robust CAPTCHA functionality
* Fully implement a 2FA protocol that would allow Poze to function as a 2FA API for sites to use, including offering alternative means of communicating with Poze (SMS or mobile app), and providing request/response patterns that align with an industry standard, if one exists. 