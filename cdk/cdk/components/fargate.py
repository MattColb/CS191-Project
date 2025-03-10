from aws_cdk import (
    aws_ecs_patterns,
    aws_ecs,
    aws_ec2,
    CfnOutput
)


def fargate_creation(scope, vpc, connection_string, lightsail_instance):
    ecs_cluster = aws_ecs.Cluster(scope, "MyEcsCluster", vpc=vpc)

    # Create a security group for the Flask service
    flask_security_group = aws_ec2.SecurityGroup(
        scope, 
        "FlaskServiceSG",
        vpc=vpc,
        description="Allow MongoDB security group to access Flask service",
        allow_all_outbound=True
    )

    # Create a docker container from the flask_docker folder
    load_balanced_fargate_service = aws_ecs_patterns.ApplicationLoadBalancedFargateService(
        scope, 
        "FargateService",
        cpu=256,
        cluster=ecs_cluster,
        memory_limit_mib=512,
        task_image_options=aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=aws_ecs.ContainerImage.from_asset("flask_docker"),
            environment={
                "MONGODB_CONN_STRING": connection_string
            }
        ),
        public_load_balancer=True,
        security_groups=[flask_security_group]
    )

    scalable_target = load_balanced_fargate_service.service.auto_scale_task_count(
        min_capacity=1,
        max_capacity=20
    )

    scalable_target.scale_on_cpu_utilization("CpuScaling",
        target_utilization_percent=50
    )

    scalable_target.scale_on_memory_utilization("MemoryScaling",
        target_utilization_percent=50
    )

    # Output the DNS where you can access your service
    output = load_balanced_fargate_service.load_balancer.load_balancer_dns_name

    CfnOutput(scope, "LoadBalancerDNS", value=output)
