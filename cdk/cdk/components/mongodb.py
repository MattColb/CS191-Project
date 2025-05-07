from aws_cdk import (
    aws_ec2,
    aws_secretsmanager,
    aws_iam,
    CfnOutput,
    aws_secretsmanager,
    aws_ssm,
)
from constructs import Construct
from dotenv import load_dotenv
import os

load_dotenv()

#The main thing that these helped with was what else I needed outside of the EC2 instance to 
#make the ec2 instance run properly and connect up with my flask application in the VPC.
#Help from: https://medium.com/@davidnsoesie1/deploying-and-configuring-mongodb-on-ec2-with-aws-cdk-2530d8d5ec17

#Help from https://bobbyhadz.com/blog/aws-cdk-ec2-instance-example

def mongo_db_creation(scope:Construct, vpc):
    #Create security group
    security_group = aws_ec2.SecurityGroup(
        scope,
        "MongoDB Security Group",
        vpc=vpc,
        allow_all_outbound=True,
    )

    #Allow mongo traffic in
    security_group.add_ingress_rule(
        peer=aws_ec2.Peer.ipv4(vpc.vpc_cidr_block),
        connection=aws_ec2.Port.tcp(27017),
        description="Allow MongoDB access from within the VPC"
    )

    #Create a role
    role = aws_iam.Role(
        scope, "MongoDBRole",
        assumed_by=aws_iam.ServicePrincipal("ec2.amazonaws.com")
    )

    #Create EC2 instance
    ec2 = aws_ec2.Instance(
        scope,
        "MongoDB",
        vpc=vpc,
        role=role,
        security_group=security_group,
        instance_type=aws_ec2.InstanceType("t2.micro"),
        machine_image=aws_ec2.MachineImage.latest_amazon_linux2023(),
        vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_EGRESS, one_per_az=True)
    )

    #Allow scripts to run on the instance
    ssmPolicyDoc = aws_iam.PolicyDocument(
        statements=[
            aws_iam.PolicyStatement(
                actions=[
                    "ssm:*",
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
    
    #Make a policy with the doc above
    ssmPolicy = aws_iam.Policy(
        scope, "MongoDBSSMPolicy",
        document=ssmPolicyDoc
    )
    role.attach_inline_policy(ssmPolicy)

    username = os.getenv("MONGODB_USER")
    password = os.getenv("MONGODB_PASS")
    #Copy it to remove the circular dependency?
    private_ip = ec2.instance_private_ip

    # User Data to install MongoDB
    #https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-amazon/
    #The
    ec2.user_data.add_commands(
        #Update and install mongo on the instance
        "sudo yum update -y",
        """sudo tee /etc/yum.repos.d/mongodb-org-8.0.repo <<EOF
[mongodb-org-8.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2023/mongodb-org/8.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://pgp.mongodb.com/server-8.0.asc
EOF""",
        "sudo yum install -y mongodb-org aws-cli jq",
        "sudo systemctl daemon-reload",
        "sudo systemctl start mongod",
        "sudo systemctl enable mongod",
        "sudo systemctl status mongod",

        "sudo chkconfig mongod on",
# Let it rest for a little bit
        "sleep 20",
        #Create a buzzy_bee_db database and a role that we can use with user that has username and password
f"""
mongosh <<EOF
use buzzy_bee_db

db.createUser({{
user: '{username}',
pwd: '{password}',
roles: [
{{ role: 'readWrite', db: 'buzzy_bee_db' }}
]
}})

EOF
""",
    "sudo sed -i 's/bindIp: 127.0.0.1/bindIp: 0.0.0.0/' /etc/mongod.conf",
    "sudo systemctl restart mongod",
    )

    #Make connection string and output it
    mongo_connection = f"mongodb://{username}:{password}@{private_ip}/buzzy_bee_db"

    CfnOutput(scope, "MongoDBConnString", value=mongo_connection)

    return security_group, mongo_connection, private_ip