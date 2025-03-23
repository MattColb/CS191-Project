from aws_cdk import (
    aws_ecs_patterns,
    aws_ecs,
    aws_ec2,
    aws_lightsail,
    CfnOutput
)


def fargate_creation(scope, connection_string, static_ip, vpc):
    ecs_cluster = aws_ecs.Cluster(scope, "MyEcsCluster", vpc=vpc)

    # Create a security group for the Flask service
    flask_security_group = aws_ec2.SecurityGroup(
        scope, 
        "FlaskServiceSG",
        vpc=vpc,
        description="Allow MongoDB security group to access Flask service",
        allow_all_outbound=True
    )

    #If this breaks, change it back to any ipv4
    flask_security_group.add_ingress_rule(
        peer=aws_ec2.Peer.ipv4(f"{static_ip.attr_ip_address}/32"),
        connection=aws_ec2.Port.tcp(27017)
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
