from aws_cdk import (
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_efs as efs,
    aws_logs as logs,
    RemovalPolicy,
    CfnOutput
)
import os

#Used copilot to help generate a base: https://github.com/copilot/share/00355124-42e4-8847-a803-3a0b84326996

def create_fargate_mongo(stack, vpc):

    # Create a cluster
    cluster = ecs.Cluster(stack, "MyCluster", vpc=vpc)

    # Create an EFS file system
    file_system = efs.FileSystem(stack, "MyEfsFileSystem",
                                    vpc=vpc,
                                    removal_policy=RemovalPolicy.DESTROY)

    # Create a task definition with a single container
    task_definition = ecs.FargateTaskDefinition(stack, "TaskDef")

    log_group = logs.LogGroup(stack, "MongoDBLogGroup", retention=logs.RetentionDays.ONE_WEEK)

    username = os.getenv("MONGODB_USER")
    password = os.getenv("MONGODB_PASS")
    database = "buzzy_bee_db"

    container = task_definition.add_container(
        "MongoDBContainer",
        image=ecs.ContainerImage.from_registry("mongo"),
        memory_limit_mib=512,
        logging=ecs.AwsLogDriver(
            log_group=log_group,
            stream_prefix="mongodb"
        ),
        environment={
            "MONGO_INITDB_ROOT_USERNAME":username,
            "MONGO_INITDB_ROOT_PASSWORD":password,
            "MONGO_INITDB_DATABASE":database
        }
    )

    container.add_port_mappings(
        ecs.PortMapping(container_port=27017)
    )

    # Define a volume
    volume_name = "MongoDBVolume"
    task_definition.add_volume(
        name=volume_name,
        efs_volume_configuration=ecs.EfsVolumeConfiguration(
            file_system_id=file_system.file_system_id
        )
    )

    # Mount the volume to the container
    container.add_mount_points(
        ecs.MountPoint(
            container_path="/data/db",
            source_volume=volume_name,
            read_only=False
        )
    )

    # Create a Fargate service and make it public
    fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
        stack, "MyFargateService",
        cluster=cluster,            # Required
        task_definition=task_definition,
        
        public_load_balancer=True   # Default is False
    )

    connection_string = f"mongodb://{username}:{password}@{fargate_service.load_balancer.load_balancer_dns_name}:27017/{database}"

    CfnOutput(stack, "MongoDBConnString", value=connection_string)

    return fargate_service, connection_string