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

    verification_lambda = aws_lambda.Function(
        scope, "BBVerificationLambda",
        runtime= aws_lambda.Runtime.PYTHON_3_10,
        handler = "verification_lambda.handler",
        code = aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), '../../../../lambdas')),
        environment = {
            "VERIFICATION_ENDPOINT":verification_endpoint+"/verify",
            "SENDER_EMAIL":sender_email
        },
        timeout=Duration.seconds(60)
    )

    verification_queue.grant_consume_messages(verification_lambda)

    verification_event_source = event_sources.SqsEventSource(verification_queue)
    verification_lambda.add_event_source(verification_event_source)

    email_queue = aws_sqs.Queue(scope, "BuzzyBee")

    email_init_lambda = aws_lambda.Function(
        scope, "BBEmailInitLambda",
        runtime= aws_lambda.Runtime.PYTHON_3_10,
        handler = "email_init_lambda.handler",
        code = aws_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), '../../../../lambdas')),
        environment = {
            "SQS_QUEUE_URL": email_queue.queue_url,
            "MONGO_CONNECTION_STRING": mongo_connection_string
        },
        timeout=Duration.seconds(300)
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
        timeout=Duration.seconds(300)
    )

    email_queue_event_source = event_sources.SqsEventSource(email_queue)
    email_processing_lambda.add_event_source(email_queue_event_source)

    email_queue.grant_consume_messages(email_processing_lambda)

    email_system_cdk_objects = cdk_object(verification_queue, verification_lambda, email_init_lambda, email_queue, email_processing_lambda)

    return email_system_cdk_objects



# CURRENT TODO:
# Code for each of the lambdas