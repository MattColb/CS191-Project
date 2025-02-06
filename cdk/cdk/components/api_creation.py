from aws_cdk import (
    aws_apigateway as apigw
)
from constructs import Construct
import uuid

def create_api(scope:Construct):
    api_key_value = str(uuid.uuid4())
    api_key = apigw.ApiKey(scope, "Main API Key", value=api_key_value)
    api = apigw.RestApi(
        scope, 
        "Testing API",
        default_cors_preflight_options={
            "allow_origins":apigw.Cors.ALL_ORIGINS,
            "allow_methods":apigw.Cors.ALL_METHODS,
            "allow_headers": ["*"],
            "status_code": 200
        },
        api_key_source_type=apigw.ApiKeySourceType.HEADER
    )
    usage_plan = api.add_usage_plan(
        "Main API Usage Plan", 
        throttle=apigw.ThrottleSettings(
            burst_limit=200,
            rate_limit=100
        )
    )
    usage_plan.add_api_stage(stage=api.deployment_stage)
    usage_plan.add_api_key(api_key)

    return api, api_key_value