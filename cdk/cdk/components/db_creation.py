from aws_cdk import (
    aws_dynamodb,
    RemovalPolicy
)

from constructs import Construct

def create_db(scope:Construct):
    ddb_table = aws_dynamodb.Table( 
        scope,
        "Testing Database",
        partition_key=aws_dynamodb.Attribute(
            name="user_id",
            type=aws_dynamodb.AttributeType.STRING
        ),
        removal_policy=RemovalPolicy.DESTROY
    )
    ddb_table.add_global_secondary_index(
        partition_key=aws_dynamodb.Attribute(
            name="username",
            type=aws_dynamodb.AttributeType.STRING
        ),
        index_name="username-index"
    )
    return ddb_table