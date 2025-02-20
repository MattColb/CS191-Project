from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2
    # aws_sqs as sqs,
)
from constructs import Construct
from cdk.components.fargate import fargate_creation
from cdk.components.mongodb import mongo_db_creation

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        #Create a documentdb with a mongodb connection and attach it to the fargate service
        vpc = aws_ec2.Vpc(self, "MyVpc", max_azs=2)

        ec2 = mongo_db_creation(self, vpc)

        # fargate_creation(self, vpc)
        