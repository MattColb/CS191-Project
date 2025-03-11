
from aws_cdk import (
    aws_ecs_patterns,
    aws_ecs,
    aws_ec2,
    CfnOutput
)


def fargate_creation(scope):
    vpc = ec2.Vpc(self, "MyVPC", max_azs=2)  
    ecs_cluster = aws_ecs.Cluster(scope, "MyEcsCluster")

    fargate_service_security_group = aws_ec2.SecurityGroup(scope, "FargateSecurityGroup",
        vpc=vpc,
        description="Allow outbound traffic to MongoDB"
    )

    # Allow Fargate to connect to MongoDB on port 27017
    fargate_service_security_group.add_egress_rule(
        peer=aws_ec2.Peer.ipv4("0.0.0.0/0"),  # Allow outbound traffic to any IP
        connection=aws_ec2.Port.tcp(27017),   # Port MongoDB uses
        description="Allow outbound traffic to MongoDB"
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
                "MONGODB_CONN_STRING":"mongodb://buzzy_bee:buzz@34.235.86.46/buzzy_bee_db"
            }
        ),
        assign_public_ip=True,
        public_load_balancer=True
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