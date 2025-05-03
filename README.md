## Buzzy Bee!

This is the repository that contains the CS191 project of Matt, Lyra, and Zosia. This is our student education system that contains games for spelling and math, a daily game called the Beedle, parent account management, teachers with classes, content, and student management, and a notification system.

To run, create an environment and activate it using the following commands

FOR MAC
```
python -m venv .venv
source .venv/bin/activate
```

FOR WINDOWS
```
python -m venv .venv
.venv\Scripts\activate
```

From there, you can deploy the CDK code if you have the npm package installed, and an AWS credentials file using

```
cdk deploy --app="{$PWD}/cdk/app.py"
```

You will also want an .env file in the root of the folder:
```
MONGODB_USER=
MONGODB_PASS=
SENDER_EMAIL=
EMAIL_API_KEY=
SPELLING_API_KEY=
```

Where the EMAIL_API_KEY is from brevo and the SPELLING_API_KEY is from words api