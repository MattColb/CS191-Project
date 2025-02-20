from aws_cdk import (
    # Duration,
    Stack,
    RemovalPolicy,
    SecretValue,
    aws_ecs_patterns,
    aws_ecs,
    CfnOutput,
    aws_ec2
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        #Create a documentdb with a mongodb connection and attach it to the fargate service
        vpc = aws_ec2.Vpc(self, "MyVpc", max_azs=2)

        #Create EC2 with mongodb
        # ec2_instance = aws_ec2.Instance(self, "MyInstance",
        #     instance_name="MyMongoDB",
        #     vpc=vpc, 
        #     instance_type=aws_ec2.InstanceType("t2.micro"),
        #     machine_image=aws_ec2.MachineImage.latest_amazon_linux(),
        #     key_name="mykey",
        #     vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PUBLIC),
        #     security_group=aws_ec2.SecurityGroup(self, "MySecurityGroup", vpc=vpc),
        #     user_data=aws_ec2.UserData.custom("yum install -y docker && service docker start && docker run -d -p 27017:27017 mongo")
        # )

        ecs_cluster = aws_ecs.Cluster(self, "MyEcsCluster", vpc=vpc)

        # Create a docker container from the flask_docker folder
        load_balanced_fargate_service = aws_ecs_patterns.ApplicationLoadBalancedFargateService(
            self, 
            "FargateService",
            cpu=256,
            cluster=ecs_cluster,
            memory_limit_mib=512,
            task_image_options=aws_ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=aws_ecs.ContainerImage.from_asset("flask_docker"),
            ),
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
        self.output = load_balanced_fargate_service.load_balancer.load_balancer_dns_name

        CfnOutput(self, "LoadBalancerDNS", value=self.output)

        