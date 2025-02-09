from aws_cdk import (
    aws_apigateway as apigw,
    aws_lambda,
    Duration,
    aws_dynamodb
)
from constructs import Construct

def create_login_system(scope:Construct, api:apigw.RestApi, ddb_table:aws_dynamodb.Table):
    login_resource = api.root.add_resource("Login")

    handler_dict = {"GET":"login_handlers.login_handler", 
                    "POST":"login_handlers.create_account", 
                    "PUT":"login_handlers.update_account_handler", 
                    "DELETE":"login_handlers.delete_account_handler"}
    lambda_handlers = []
    for (method, handler) in handler_dict.items():
        current_fn = aws_lambda.Function(
            scope, 
            "Hello World API Endpoint", 
            code = aws_lambda.Code.from_asset("../api_functions"),
            runtime=aws_lambda.Runtime.PYTHON_3_10,
            handler=handler,
            timeout = Duration.seconds(300),
            environment={
                "DYNAMODB_TABLE_NAME":ddb_table.table_name
            }
        )

        lambda_handlers.append(current_fn)
        login_resource.add_method(method, apigw.LambdaIntegration(current_fn))