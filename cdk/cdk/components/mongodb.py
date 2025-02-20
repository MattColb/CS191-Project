from aws_cdk import (
    aws_ec2,
    aws_secretsmanager,
    aws_iam,

)
from constructs import Construct

#Help from: https://medium.com/@davidnsoesie1/deploying-and-configuring-mongodb-on-ec2-with-aws-cdk-2530d8d5ec17


def mongo_db_creation(stack:Construct, vpc):

    security_group = aws_ec2.SecurityGroup(
        stack, 
        "MongoDBSecurityGroup",
        vpc=vpc
    )

    role = aws_iam.Role(
        stack, "MongoDBRole",
        assumed_by=aws_iam.ServicePrincipal("ec2.amazonaws.com")
    )

    key_name = "MongoDBKeyPair"

    key_pair = aws_ec2.KeyPair(
        stack, "MongoDBKeyPair",
        key_pair_name=key_name,
        format=aws_ec2.KeyPairFormat.PEM,
        type=aws_ec2.KeyPairType.RSA
    )

    # Create a documentdb with a mongodb connection and attach it to the fargate service
    ec2 = aws_ec2.Instance(
        stack, "MongoDB",
        instance_type=aws_ec2.InstanceType("t2.micro"),
        machine_image=aws_ec2.MachineImage.latest_amazon_linux2(),
        vpc=vpc,
        role=role,
        key_pair=key_pair,
        security_group=security_group,
        block_devices=[
            aws_ec2.BlockDevice(
                device_name="/dev/xvda",
                volume=aws_ec2.BlockDeviceVolume.ebs(
                    volume_size=20
                )
            )
        ]
    )

    credentials = aws_secretsmanager.Secret(
        stack,
        "MongoDBSecret",
        generate_secret_string=aws_secretsmanager.SecretStringGenerator(
            secret_string_template='{"username": "admin"}',
            generate_string_key="password",
            password_length=12,
            exclude_characters='"/@'
        )
    )

    credentials.grant_read(role)

    ssmPolicyDoc = aws_iam.PolicyDocument(
        statements=[
            aws_iam.PolicyStatement(
                actions=[
                    "ssm:GetParameter",
                    "ssm:GetParameters",
                    "ssm:GetParametersByPath",
                    "ssm:UpdateInstanceInformation",
                    "ssmmessages:CreateControlChannel",
                    "ssmmessages:CreateDataChannel",
                    "ssmmessages:OpenControlChannel",
                    "ssmmessages:OpenDataChannel",
                ],
                resources=[
                    "*"
                ]
            )
        ]
    )
    
    ssmPolicy = aws_iam.Policy(
        stack, "MongoDBSSMPolicy",
        document=ssmPolicyDoc
    )

    role.attach_inline_policy(ssmPolicy)

    security_group.add_ingress_rule(
        peer=aws_ec2.Peer.any_ipv4(),
        connection=aws_ec2.Port.tcp(27017),
        description="Allow MongoDB access from within the VPC"
    )
    
    # Run script here
    ec2.user_data.add_commands(
        "yum install -y amazon-linux-extras",
        "amazon-linux-extras enable mongodb4.0",
        "yum install -y mongodb-org",
        "service mongod start"
    )