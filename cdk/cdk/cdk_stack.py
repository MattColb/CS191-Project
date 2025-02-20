from aws_cdk import (
    # Duration,
    Stack,
    RemovalPolicy,
    SecretValue,
    aws_ecs_patterns,
    aws_ecs,
    CfnOutput,
    aws_docdb as docdb,
    aws_ec2
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )


        #Create a documentdb with a mongodb connection and attach it to the fargate service
        vpc = aws_ec2.Vpc(self, "MyVpc", max_azs=2)

        # Create a DocumentDB cluster
        # db_cluster = docdb.DatabaseCluster(
        #     self, "MyDocDBCluster",
        #     master_user=docdb.Login(
        #         username="docdb_admin",
        #         secret_name="/myapp/mydocdb/masteruser"
        #     ),
        #     instance_type=aws_ec2.InstanceType.of(
        #         aws_ec2.InstanceClass.BURSTABLE2, 
        #         aws_ec2.InstanceSize.SMALL
        #     ),
        #     vpc=vpc,
        #     removal_policy=RemovalPolicy.DESTROY,
            
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
                # environment={
                #     "MONGO_URI": f"mongodb://{db_cluster.cluster_endpoint.hostname}:27017"
                # }
            ),
            public_load_balancer=True
        )

        # db_cluster.connections.allow_default_port_from(load_balanced_fargate_service.service)

        #Give the db cluster the ability to be accessed from my local computer
        # db_cluster.connections.allow_default_port_from_any_ipv4()

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

        