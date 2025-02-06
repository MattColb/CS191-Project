from aws_cdk import (
    aws_apigateway as apg,
    aws_lambda, 
    Duration,
    aws_dynamodb
)
from constructs import Construct

def create_hello_resource(scope:Construct, api:apg.RestApi, ddb_table:aws_dynamodb.Table):
    hello_fn = aws_lambda.Function(
        scope, 
        "Hello World API Endpoint", 
        code = aws_lambda.Code.from_asset("../api_functions"),
        runtime=aws_lambda.Runtime.PYTHON_3_10,
        handler="hello.handler",
        timeout = Duration.seconds(300),
        environment={
            "DYNAMODB_TABLE_NAME":ddb_table.table_name
        }
    )

    hello_resource = api.root.add_resource("Hello")
    ddb_table.grant_read_data(hello_fn)

    hello_resource.add_method(
        "GET", 
        apg.LambdaIntegration(hello_fn), 
        api_key_required=True,
        request_parameters={"method.request.header.x-api-key":True}
    )

    hello_post_fn = aws_lambda.Function(
        scope, 
        "Testing Post API Endpoint", 
        code = aws_lambda.Code.from_asset("../api_functions"),
        runtime=aws_lambda.Runtime.PYTHON_3_10,
        handler="test_post.handler",
        timeout = Duration.seconds(300),
        environment={
            "DYNAMODB_TABLE_NAME":ddb_table.table_name
        }
    )

    ddb_table.grant_read_write_data(hello_post_fn)
    hello_resource.add_method(
        "POST", 
        apg.LambdaIntegration(hello_post_fn), 
        api_key_required=True,
        request_parameters={"method.request.header.x-api-key":True}
    )