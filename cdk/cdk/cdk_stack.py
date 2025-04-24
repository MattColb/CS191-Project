from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2,
    aws_sqs
    # aws_sqs as sqs,
)
from constructs import Construct
from cdk.components.lightsail_mongo import create_mongo
from cdk.components.fargate import fargate_creation
from cdk.components.email_components.notification_system import create_notification_system
from dotenv import load_dotenv
import os

load_dotenv()

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC for the ECS cluster
        vpc = aws_ec2.Vpc(self, "MyVpc", max_azs=2)

        mongo_connection, static_ip = create_mongo(self, vpc)
        
        verification_queue = aws_sqs.Queue(self, "BuzzyBeeVerificationQueue")

        api_key = os.getenv("SPELLING_API_KEY")

        url = fargate_creation(self, mongo_connection, static_ip, vpc, verification_queue, api_key)

        components = create_notification_system(self, mongo_connection, url, verification_queue)