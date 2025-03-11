import aws_cdk as cdk
from constructs import Construct
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_iam as iam
import aws_cdk.custom_resources as cr
import aws_cdk.aws_ecr_assets as ecr_assets

# Help from: https://claude.site/artifacts/e89e294f-5610-4aa5-a7a1-051bd6854628

def flask_light_sail(scope, connection_string):
    # Custom resource to create and deploy the Lightsail container service
    lightsail_container = cr.AwsCustomResource(scope, "LightsailContainer",
        on_create={
            "service": "lightsail",
            "action": "createContainerService",
            "parameters": {
                "serviceName": "flask-app",
                "power": "micro",
                "scale": 1
            },
            "physical_resource_id": cr.PhysicalResourceId.from_response("containerService.containerServiceName")
        },
        policy=cr.AwsCustomResourcePolicy.from_sdk_calls(resources=cr.AwsCustomResourcePolicy.ANY_RESOURCE)
    )

    image = ecr_assets.DockerImageAsset(scope, "FlaskDockerImage",
        directory="flask_docker" 
    )

    # Custom resource to deploy the container
    lightsail_deployment = cr.AwsCustomResource(scope, "LightsailDeployment",
        on_create={
            "service": "lightsail",
            "action": "createContainerServiceDeployment",
            "parameters": {
                "serviceName": "flask-app",
                "containers": {
                    "flask": {
                        "image": f"{image.image_uri}:latest",
                        "environment": {
                            "MONGODB_CONN_STRING": connection_string
                        },
                        "ports": {
                            "80": "HTTP"
                        }
                    }
                },
                "publicEndpoint": {
                    "containerName": "flask",
                    "containerPort": 80
                }
            },
            "physical_resource_id": cr.PhysicalResourceId.of("flask-app-deployment")
        },
        policy=cr.AwsCustomResourcePolicy.from_sdk_calls(resources=cr.AwsCustomResourcePolicy.ANY_RESOURCE)
    )

    # Deployment depends on container service
    lightsail_deployment.node.add_dependency(lightsail_container)

    # Get the URL of the service
    get_service_url = cr.AwsCustomResource(scope, "GetServiceUrl",
        on_create={
            "service": "lightsail",
            "action": "getContainerServices",
            "parameters": {
                "serviceName": "flask-app"
            },
            "physical_resource_id": cr.PhysicalResourceId.of("flask-app-url")
        },
        policy=cr.AwsCustomResourcePolicy.from_sdk_calls(resources=cr.AwsCustomResourcePolicy.ANY_RESOURCE)
    )
    get_service_url.node.add_dependency(lightsail_deployment)

    # Output the public URL
    url = get_service_url.get_response_field("containerServices.0.url")
    cdk.CfnOutput(scope, "ServiceUrl",
        value=f"https://{url}",
        description="URL of the Flask application"
    )