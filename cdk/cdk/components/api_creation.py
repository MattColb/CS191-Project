from aws_cdk import (
    aws_apigateway as apigw
)
from constructs import Construct

def create_api(scope:Construct):
    api = apigw.RestApi(
        scope, 
        "Testing API"
    )
    # Add an API key here as well?

    return api