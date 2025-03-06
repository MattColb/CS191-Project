from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2,
    aws_iam
    # aws_sqs as sqs,
)
from constructs import Construct
from cdk.components.mongodb import mongo_db_creation
from cdk.components.fargate import fargate_creation
from cdk.components.fargate_mongo import create_fargate_mongo


class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        #Create a VPC
        vpc = aws_ec2.Vpc(
            self,
            "VPC",
            max_azs=2,
            nat_gateways=1,
            subnet_configuration=[
                aws_ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=aws_ec2.SubnetType.PUBLIC
                )
            ]
        )

        fargate, mongo_connection = create_fargate_mongo(self, vpc)

        #Creating the mongodb ec2
        # ec2, mongo_connection = mongo_db_creation(self, vpc)

        fargate_creation(self, vpc, mongo_connection)