from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2,
    aws_iam
    # aws_sqs as sqs,
)
from constructs import Construct
from cdk.components.fargate import fargate_creation
from cdk.components.lightsail_mongo import create_mongo
from cdk.components.lightsail_mongo_public import create_mongo_public

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        # Create a VPC
        # vpc = aws_ec2.Vpc(
        #     self,
        #     "VPC",
        #     max_azs=2,
        #     nat_gateways=1,
        #     subnet_configuration=[
        #         aws_ec2.SubnetConfiguration(
        #             name="Public",
        #             subnet_type=aws_ec2.SubnetType.PUBLIC
        #         ),
        #         aws_ec2.SubnetConfiguration(
        #             name="Private",
        #             subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_EGRESS
        #         )
        #     ]
        # )
        # mongo_connection, lightsail_instance = create_mongo(self)

        # fargate_creation(self, vpc, mongo_connection, lightsail_instance)

        mongo_connection_public, lightsail_instance_public = create_mongo_public(self)