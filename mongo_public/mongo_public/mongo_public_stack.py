from aws_cdk import (
    Stack,
)
from constructs import Construct
from .components.lightsail_mongo_public import create_mongo_public

class MongoPublicStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        connection_string, instance = create_mongo_public(self)