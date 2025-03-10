from aws_cdk import (
    aws_lightsail,
    aws_ecs
)

def lightsail_flask_creation(scope, connection_string):

    container = aws_lightsail.CfnContainer(
        scope,
        "BuzzyBeeContainer",
        container_service_deployment=aws_lightsail.CfnContainer.ContainerServiceDeploymentProperty(
            containers=[
                aws_lightsail.CfnContainer.ContainerProperty(
                    command=["python3", "app.py"],
                    environment=aws_lightsail.CfnContainer.ContainerServiceEnvironmentProperty(
                        MONGODB_CONN_STRING=connection_string
                    ),
                    image=aws_ecs.ContainerImage.from_asset("flask_docker"),
                    container_name="flask"
                )
            ],
            public_endpoint=aws_lightsail.CfnContainer.EndpointRequestProperty(
                container_name="flask",
                container_port=80
            )
        )
    )