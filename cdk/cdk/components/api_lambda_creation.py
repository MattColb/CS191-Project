from aws_cdk import (
    aws_apigateway as apg,
    aws_lambda, 
    Duration,
    aws_dynamodb
)
from constructs import Construct
from .api_components.login import *

def create_api_resources(scope:Construct, api:apg.RestApi, ddb_table:aws_dynamodb.Table):
    create_login_system(scope, api, ddb_table)