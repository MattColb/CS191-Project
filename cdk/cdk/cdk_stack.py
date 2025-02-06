from aws_cdk import (
    Stack,
    CfnOutput,
    aws_s3
)
from constructs import Construct
from .components.api_creation import create_api
from .components.api_lambda_creation import create_hello_resource
from .components.frontend_creation import create_frontend_bucket
from .components.db_creation import create_db

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        
        api, api_key_value = create_api(self)
        ddb_table = create_db(self)
        create_hello_resource(self, api, ddb_table)
        bucket:aws_s3.Bucket = create_frontend_bucket(self, api, api_key_value)

        CfnOutput(self, "Website Output", bucket.bucket_website_url)