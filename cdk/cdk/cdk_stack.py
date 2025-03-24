from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2,
    aws_iam
    # aws_sqs as sqs,
)
from constructs import Construct
from cdk.components.lightsail_mongo import create_mongo
from cdk.components.lightsail_mongo_public import create_mongo_public
from cdk.components.fargate import fargate_creation

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a VPC for the ECS cluster
        vpc = aws_ec2.Vpc(self, "MyVpc", max_azs=2)

        mongo_connection_public, lightsail_instance_public = create_mongo_public(self)

        mongo_connection, static_ip = create_mongo(self, vpc)


        fargate_creation(self, mongo_connection, static_ip, vpc)
