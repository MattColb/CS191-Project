from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2,
    aws_iam
    # aws_sqs as sqs,
)
from constructs import Construct
from cdk.components.lightsail_mongo import create_mongo
from cdk.components.eks_flask import flask_light_sail

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        mongo_connection, lightsail_instance = create_mongo(self)

        flask_light_sail(self, mongo_connection)

        # mongo_connection_public, lightsail_instance_public = create_mongo_public(self)