from aws_cdk import (
    aws_sqs,
    aws_lambda,
    Duration,
    aws_events as events,
    aws_events_targets as targets,
    aws_lambda_event_sources as event_sources
)
from return_object import cdk_object
import os
from dotenv import load_dotenv
import subprocess

# Ref: https://cloudbytes.dev/aws-academy/using-lambda-layers-with-aws-cdk-in-python
def create_lambda_layer(self):
    requirements_file = "lambda_requirements.txt"
    output_dir = ".build/app"
    path_to_db_functions = os.path.join(os.path.dirname(__file__), '../../../../flask_docker/buzzy_bee_db')

    if not os.environ.get("SKIP_PIP"):
        subprocess.check_call(f"pip install -r {requirements_file} -t {output_dir}/python".split()) #Install what is in requirements
        subprocess.check_call(f"pip install --upgrade {path_to_db_functions} -t {output_dir}/python".split())  # Install the db_functions

    layer_code = aws_lambda.Code.from_asset(output_dir)
    return aws_lambda.LayerVersion(self.scope, "Lambda DB Layer", code=layer_code)

# Used chatgpt to see how to move from SNS to a more individualized method in SES: https://chatgpt.com/share/67e4a548-4930-8013-8a80-5fd29127de63

#Need to add one more thing to give web application access to the SQS queue
def create_notification_system(scope, mongo_connection_string, verification_endpoint, verification_queue):

    # SQS Queue that app puts into
    # Sends out a verification email
    # Once verified, they are added to the email weekly list (verification endpoint)
    # A lambda is triggered once a week to get all of the emails and add them to a queue
    # Another lambda injests from the queue, sending an email to the email in the queue

    load_dotenv(os.path.join(os.path.dirname(__file__), '../../../../.env'))

    sender_email = os.getenv("SENDER_EMAIL")

    lambda_role = iam.Role(
        self, "EmailLambdaRole",
        assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
        managed_policies=[
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
        ]
    )

    # Allow Lambda to send emails via SES
    lambda_role.add_to_policy(
        iam.PolicyStatement(
            actions=["ses:SendEmail", "ses:SendRawEmail"],
            resources=["*"]
        )
    )

    verification_lambda = aws_lambda.Function(
        scope, "BBVerificationLambda",
        runtime= aws_lambda.Runtime.PYTHON_3_10,
        handler = "verification_lambda.handler",
        code = aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), '../../../../lambdas')),
        environment = {
            "VERIFICATION_ENDPOINT":verification_endpoint+"/verify",
            "SENDER_EMAIL":sender_email
        },
        timeout=Duration.seconds(60),
        role=lambda_role
    )

    verification_queue.grant_consume_messages(verification_lambda)

    verification_event_source = event_sources.SqsEventSource(verification_queue)
    verification_lambda.add_event_source(verification_event_source)

    email_queue = aws_sqs.Queue(scope, "BuzzyBee")

    lambda_layer = create_lambda_layer(scope)

    email_init_lambda = aws_lambda.Function(
        scope, "BBEmailInitLambda",
        runtime= aws_lambda.Runtime.PYTHON_3_10,
        handler = "email_init_lambda.handler",
        code = aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), '../../../../lambdas')),
        environment = {
            "SQS_QUEUE_URL": email_queue.queue_url,
            "MONGO_CONNECTION_STRING": mongo_connection_string
        },
        timeout=Duration.seconds(300),
        layers=[lambda_layer],
        role=lambda_role
    )

    email_queue.grant_send_messages(email_init_lambda)

    rule = events.Rule(
        scope, "WeeklyEmailRule",
        schedule=events.Schedule.expression("rate(7 days)"),
    )
    rule.add_target(targets.LambdaFunction(email_init_lambda))

    email_processing_lambda = aws_lambda.Function(
        scope, "BBEmailProcessQueue",
        runtime= aws_lambda.Runtime.PYTHON_3_10,
        handler = "email_handler.handler",
        code = aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), '../../../../lambdas')),
        environment = {
            "MONGO_CONNECTION_STRING": mongo_connection_string,
            "SENDER_EMAIL":sender_email
        },
        timeout=Duration.seconds(300),
        layers=[lambda_layer],
        role=lambda_role
    )

    email_queue_event_source = event_sources.SqsEventSource(email_queue)
    email_processing_lambda.add_event_source(email_queue_event_source)

    email_queue.grant_consume_messages(email_processing_lambda)

    email_system_cdk_objects = cdk_object(verification_queue, verification_lambda, email_init_lambda, email_queue, email_processing_lambda)

    return email_system_cdk_objects



# CURRENT TODO:
# Code for each of the lambdas