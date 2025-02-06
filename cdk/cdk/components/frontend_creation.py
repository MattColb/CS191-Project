from aws_cdk import (
    aws_apigateway as apg,
    aws_s3,
    RemovalPolicy,
    aws_s3_deployment
)
from constructs import Construct
import json
import os

def create_frontend_bucket(scope:Construct, api:apg.RestApi, api_key_value):
    s3_bucket = aws_s3.Bucket(
        scope, 
        "Frontend Website Bucket", 
        removal_policy=RemovalPolicy.DESTROY,
        public_read_access=True,
        website_index_document="index.html",
        block_public_access=aws_s3.BlockPublicAccess.BLOCK_ACLS,
        auto_delete_objects=True
    )

    json_api_url = json.dumps({"api_url":api.url, "api_key":api_key_value})

    aws_s3_deployment.BucketDeployment(
        scope,
        "Frontend Deployment",
        sources = [
            aws_s3_deployment.Source.asset(os.path.join(os.path.dirname(__file__), "../../../frontend")),
            aws_s3_deployment.Source.data("api_info.json", json_api_url)
            ],
        destination_bucket=s3_bucket
    )