from aws_cdk import (
    aws_apigateway as apigw,
    aws_lambda,
    Duration,
    aws_dynamodb
)
from constructs import Construct
import os, subprocess
from cdk.components.api_structure import API_STRUCTURE
import copy

class Resource_Items:
    def __init__(self, scope, api, ddb_table):
        self.scope = scope
        self.api = api
        self.ddb_table = ddb_table
        self.lambda_layer = self.create_lambda_layer()

    # Ref: https://cloudbytes.dev/aws-academy/using-lambda-layers-with-aws-cdk-in-python
    def create_lambda_layer(self):
        requirements_file = "api_functions/requirements.txt"
        output_dir = ".build/app"
        path_to_db_functions = "buzzy_bee_db/"

        if not os.environ.get("SKIP_PIP"):
            subprocess.check_call(f"pip install -r {requirements_file} -t {output_dir}/python".split()) #Install what is in requirements
            subprocess.check_call(f"pip install --upgrade {path_to_db_functions} -t {output_dir}/python".split())  # Install the db_functions

        layer_code = aws_lambda.Code.from_asset(output_dir)
        return aws_lambda.LayerVersion(self.scope, "Lambda DB Layer", code=layer_code)

def create_api_resources(scope:Construct, api:apigw.RestApi, ddb_table:aws_dynamodb.Table):
    ri = Resource_Items(scope, api, ddb_table)
    root = api.root
    resources = copy.deepcopy(API_STRUCTURE)
    recursive_call(API_STRUCTURE, root, "/", resources, ri)
    return resources


def recursive_call(structure_dictionary, previous_resource, current_resource_name, resource_dict, resource_items):
    for (key, value) in structure_dictionary.items():
        if isinstance(value, str):
            create_endpoint(
                value, 
                key, 
                previous_resource, 
                current_resource_name, 
                resource_dict,
                resource_items
            )
        else:
            current_resource = previous_resource.add_resource(key)
            current_resource_dict = resource_dict.get(key)
            recursive_call(value, current_resource, key, current_resource_dict, resource_items)

def create_endpoint(
    handler, 
    method,
    current_resource,
    current_resource_name, 
    resource_dict,
    resource_items
    ):
    api = resource_items.api
    ddb_table = resource_items.ddb_table
    scope = resource_items.scope
 
    current_fn = aws_lambda.Function(
        scope, 
        f"{current_resource_name}-{method}-ENDPOINT",
        code = aws_lambda.Code.from_asset(os.path.join(__file__, "../../../../api_functions")),
        runtime=aws_lambda.Runtime.PYTHON_3_10,
        handler=handler,
        timeout = Duration.seconds(300),
        environment={
            "DYNAMODB_TABLE_NAME":ddb_table.table_name
        },
        layers=[resource_items.lambda_layer]
    )

    current_method = current_resource.add_method(
        method, 
        apigw.LambdaIntegration(current_fn),
        api_key_required=True,
        request_parameters={"method.request.header.x-api-key":True}
    )

    ddb_table.grant_read_write_data(current_fn)
    resource_dict[method] = {"lambda":current_fn, "method":current_method, "resource":current_resource}