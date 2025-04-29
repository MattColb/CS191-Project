from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2,
    aws_sqs
    # aws_sqs as sqs,
)
from constructs import Construct
# from cdk.components.lightsail_mongo import create_mongo
from cdk.components.mongodb import mongo_db_creation
from cdk.components.fargate import fargate_creation
from cdk.components.email_components.notification_system import create_notification_system
from dotenv import load_dotenv
import os

load_dotenv()

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC for the ECS cluster
        #Add subnet configurations
        vpc = aws_ec2.Vpc(self, 
                          "MyVpc", 
                          max_azs=2,
                          subnet_configuration=[
                                aws_ec2.SubnetConfiguration(
                                    name="Public",
                                    subnet_type=aws_ec2.SubnetType.PUBLIC,
                                    cidr_mask=24
                                ),
                                aws_ec2.SubnetConfiguration(
                                    name="Private",
                                    subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_EGRESS,
                                    cidr_mask=24
                                ),
                                aws_ec2.SubnetConfiguration(
                                    name="Isolated",
                                    subnet_type=aws_ec2.SubnetType.PRIVATE_ISOLATED,
                                    cidr_mask=24
                                )
                          ]
                          )

        ec2_instance, mongo_connection, private_ip = mongo_db_creation(self, vpc)
        
        verification_queue = aws_sqs.Queue(self, "BuzzyBeeVerificationQueue")

        api_key = os.getenv("SPELLING_API_KEY")

        url = fargate_creation(self, mongo_connection, private_ip, vpc, verification_queue, api_key)

        components = create_notification_system(self, mongo_connection, url, verification_queue, vpc)