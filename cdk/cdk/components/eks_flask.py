from aws_cdk import (
    aws_elasticbeanstalk as eb,
    aws_iam as iam,
    aws_ec2 as ec2,
    aws_ecr_assets as ecr_assets
)


def flask_light_sail(scope, connection_string):
    docker_image = ecr_assets.DockerImageAsset(scope, "FlaskDockerImage",
                                                   directory="./app")  
    # Define Elastic Beanstalk application
    app = eb.CfnApplication(scope, "FlaskApp",
                            application_name="FlaskApp")

    # Define IAM role for Elastic Beanstalk
    role = iam.Role(scope, "ElasticBeanstalkRole",
                    assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"))

    role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name(
        "AWSElasticBeanstalkWebTier"))

    # Elastic Beanstalk instance profile
    instance_profile = iam.CfnInstanceProfile(scope, "InstanceProfile",
                                                roles=[role.role_name])

    # Define environment variables
    environment_vars = [
        {"name": "MONGO_URI", "value": connection_string}
    ]

    # Elastic Beanstalk Environment
    env = eb.CfnEnvironment(scope, "FlaskAppEnv",
                            application_name=app.application_name,
                            environment_name="FlaskAppEnv",
                            solution_stack_name="64bit Amazon Linux 2 v5.8.1 running Docker",
                            option_settings=[
                                {"namespace": "aws:elasticbeanstalk:application:environment",
                                    "option_name": var["name"],
                                    "value": var["value"]
                                    } for var in environment_vars
                            ],
                            instance_profile=instance_profile.instance_profile_name)