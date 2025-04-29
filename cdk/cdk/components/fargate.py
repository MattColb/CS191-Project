from aws_cdk import (
    aws_ecs_patterns,
    aws_ecs,
    aws_ec2,
    aws_iam,
    CfnOutput
)

#CHANGED: Remove Nat, Added Task Subnet, added vpc in fargate service rather than is aws_ecs.cluster


def fargate_creation(scope, mongo_connection, private_ip, vpc, verification_queue, api_key, mongo_security_group):
    # Create a security group for the Flask service
    flask_security_group = aws_ec2.SecurityGroup(
        scope, 
        "FlaskServiceSG",
        vpc=vpc,
        description="Allow MongoDB security group to access Flask service",
        allow_all_outbound=True
    )

    mongo_security_group.add_ingress_rule(
        peer=flask_security_group,  # Allow traffic from the Fargate service's security group
        connection=aws_ec2.Port.tcp(27017),
        description="Allow Fargate service to connect to MongoDB"
    )

    #If this breaks, change it back to any ipv4
    flask_security_group.add_ingress_rule(
        peer=aws_ec2.Peer.ipv4(f"{private_ip}/32"),
        connection=aws_ec2.Port.tcp(27017)
    )

    flask_security_group.add_egress_rule(
        peer=aws_ec2.Peer.ipv4(f"{private_ip}/32"),
        connection=aws_ec2.Port.tcp(27017)
    )

    # Create a docker container from the flask_docker folder
    
    load_balanced_fargate_service = aws_ecs_patterns.ApplicationLoadBalancedFargateService(
        scope, 
        "FargateService",
        cpu=256,
        memory_limit_mib=512,
        task_image_options=aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
            image=aws_ecs.ContainerImage.from_asset("flask_docker"),
            environment={
                "MONGODB_CONN_STRING": mongo_connection,
                "SQS_QUEUE_URL":verification_queue.queue_url,
                "SPELLING_API_KEY":api_key
            }
        ),
        public_load_balancer=True,
        security_groups=[flask_security_group],
        task_subnets=aws_ec2.SubnetSelection(
            subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_EGRESS,
            one_per_az=True
        ),
        vpc=vpc,
        assign_public_ip=True,
        desired_count=1,
    )

    #Questionable, but could work
    load_balanced_fargate_service.task_definition.add_to_task_role_policy(
        aws_iam.PolicyStatement(
            actions=["sqs:SendMessage"],
            resources=[verification_queue.queue_arn]
        )
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

    return output