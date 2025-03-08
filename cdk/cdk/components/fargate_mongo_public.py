from aws_cdk import (
    aws_ecs as ecs,
    aws_ec2,
    CfnOutput,
    aws_efs,
    RemovalPolicy,
    aws_iam as iam,
    aws_elasticloadbalancingv2 as elbv2
)
import os

def create_fargate_mongo_public(stack, vpc):

    username = os.environ["MONGODB_USERNAME"]
    password = os.environ["MONGODB_PASSWORD"]
    database = os.environ["MONGODB_DATABASE"]

    #Create a container Cluster
    ecs_cluster = ecs.Cluster(stack, "MongoDBECSClusterPUBLIC", vpc=vpc)
    

    task_role = iam.Role(
        stack, "MongoDBTaskRolePUBLIC",
        assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com")
    )

    # Allow ECS tasks to access EFS
    task_role.add_managed_policy(
        iam.ManagedPolicy.from_aws_managed_policy_name("AmazonElasticFileSystemClientReadWriteAccess")
    )

    efs_security_group = aws_ec2.SecurityGroup(
        stack, "EFSSecurityGroupPUBLIC",
        vpc=vpc,
        allow_all_outbound=True
    )

    efs_security_group.add_ingress_rule(
        peer=aws_ec2.Peer.ipv4(vpc.vpc_cidr_block),  # Allow only internal traffic
        connection=aws_ec2.Port.tcp(2049),
    )


    #Create a Fargate Task Definition
    task_definition = ecs.FargateTaskDefinition(
        stack, "MongoDBTaskDefPUBLIC",
        cpu=256,
        memory_limit_mib=512,
        task_role=task_role
    )

    #Filesystem volume for the MongoDB container
    mongo_persistent_storage = aws_efs.FileSystem(
        stack, "MongoDBFileSystemPUBLIC",
        vpc=vpc,
        removal_policy=RemovalPolicy.DESTROY,
        security_group=efs_security_group
    )

    #Create an access point for the mongodb
    storage_access_point = mongo_persistent_storage.add_access_point(
        "MongoDBAccessPointPUBLIC",
        path="/bitnami/mongodb",
        create_acl=aws_efs.Acl(owner_gid="1000", owner_uid="1000", permissions="777")
    )

    #Add the volume to the task definition
    task_definition.add_volume(
        name="MongoDBVolumePUBLIC",
        efs_volume_configuration=ecs.EfsVolumeConfiguration(
            file_system_id=mongo_persistent_storage.file_system_id,
            transit_encryption="ENABLED",
            authorization_config=ecs.AuthorizationConfig(
                access_point_id=storage_access_point.access_point_id,
                iam="DISABLED"
            )
        )
    )

    #Add the mongodb container to the task definition
    container = task_definition.add_container(
        "MongoDBContainerPUBLIC",
        image=ecs.ContainerImage.from_registry("public.ecr.aws/bitnami/mongodb:4.4"),
        environment={
            "MONGODB_ROOT_PASSWORD": os.getenv("MONGODB_ROOT_PASSWORD"),
            "MONGODB_USERNAME": username,
            "MONGODB_PASSWORD": password,
            "MONGODB_DATABASE": database
        }
    )

    container.add_mount_points(
        ecs.MountPoint(
            container_path="/bitnami/mongodb",
            source_volume="MongoDBVolumePUBLIC",
            read_only=False
        )
    )

    #Map the container so that the internal port and external port are the same
    container.add_port_mappings(
        ecs.PortMapping(
            container_port=27017,
            host_port=27017
        )
    )

    #Create a security group for the MongoDB container
    mongo_security_group = aws_ec2.SecurityGroup(
        stack, "MongoDBSecurityGroupPUBLIC",
        vpc=vpc,
        allow_all_outbound=True
    )

    #Allow traffic to the MongoDB container from the VPC
    mongo_security_group.add_ingress_rule(
        peer=aws_ec2.Peer.any_ipv4(),
        connection=aws_ec2.Port.tcp(27017)
    )

    mongo_security_group.add_egress_rule(
        peer=efs_security_group,
        connection=aws_ec2.Port.tcp(2049)
    )

    #Create a Fargate Service
    fargate_service = ecs.FargateService(
        stack, "MongoDBFargateServicePUBLIC",
        cluster=ecs_cluster,
        task_definition=task_definition,
        desired_count=1,
        vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PUBLIC),
        assign_public_ip=True,
        security_groups=[mongo_security_group]
    )

    #ADDING A PUBLIC IP

    #Create a load balancer
    lb = elbv2.ApplicationLoadBalancer(
        stack, "MongoDBLoadBalancerPUBLIC",
        vpc=vpc,
        internet_facing=True
    )

    #Create a listener
    listener = lb.add_listener(
        "MongoDBListenerPUBLIC",
        port=80,
        open=True
    )

    #Add the Fargate service as a target
    listener.add_targets(
        "MongoDBFargateServiceTargetPUBLIC",
        port=80,
        targets=[fargate_service.load_balancer_target(container_name="MongoDBContainerPUBLIC", container_port=27017)]
    )

    #Output the connection string
    CfnOutput(
        stack, "MongoDBConnectionStringPUBLIC",
        value=f"mongodb://{username}:{password}@{lb.load_balancer_dns_name}:80/{database}"
    )