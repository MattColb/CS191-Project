from aws_cdk import (
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_efs as efs,
    RemovalPolicy,
    CfnOutput
)
import os

#Used copilot to help generate a base: https://github.com/copilot/share/00355124-42e4-8847-a803-3a0b84326996

def create_fargate_mongo(stack, vpc):

    username = os.environ["MONGODB_USERNAME"]
    password = os.environ["MONGODB_PASSWORD"]
    database = os.environ["MONGODB_DATABASE"]

    #Creating a MongoDB Fargate Service
    fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
        stack, "MongoDBFargateService",
        cpu=512,
        memory_limit_mib=2048,
        task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=ecs.ContainerImage.from_registry("public.ecr.aws/bitnami/mongodb:4.4"),
            container_port=27017,
            environment={
                "MONGODB_ROOT_PASSWORD": os.environ["MONGODB_ROOT_PASSWORD"],
                "MONGODB_USERNAME": username,
                "MONGODB_PASSWORD": password,
                "MONGODB_DATABASE": database
            }
        ),
        public_load_balancer=True,
        vpc=vpc
    )

    connection_string = f"mongodb://{username}:{password}@{fargate_service.load_balancer.load_balancer_dns_name}:27017/{database}"

    CfnOutput(stack, "MongoDBConnString", value=connection_string)

    return fargate_service, connection_string