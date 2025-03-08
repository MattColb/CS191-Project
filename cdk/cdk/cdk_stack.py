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
from cdk.components.fargate_mongo_public import create_fargate_mongo_public



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
                ),
                aws_ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_EGRESS
                )
            ]
        )
        # create_fargate_mongo_public(self, vpc)
        mongo_connection, mongo_security_group = create_fargate_mongo(self, vpc)

        #Creating the mongodb ec2
        # ec2, mongo_connection = mongo_db_creation(self, vpc)

        # mongo_connection = "mongodb://buzzy_bee:buzz@34.201.146.136/buzzy_bee_db"
        fargate_creation(self, vpc, mongo_connection, mongo_security_group)