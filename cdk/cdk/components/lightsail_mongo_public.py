from aws_cdk import (
    aws_lightsail,
    CfnOutput,
    aws_ec2
)
from dotenv import load_dotenv
import os

load_dotenv()


def create_mongo_public(scope):

    username = os.getenv("MONGODB_USER")
    password = os.getenv("MONGODB_PASS")


    instance = aws_lightsail.CfnInstance(
        scope,
        "MongoDBInstancePublic",
        instance_name="MongoDBInstancePublic",
        blueprint_id="amazon_linux_2023",
        bundle_id="micro_3_0",
        availability_zone="us-east-1a",
        networking=aws_lightsail.CfnInstance.NetworkingProperty(
            ports=[
                aws_lightsail.CfnInstance.PortProperty(
                    from_port=22,
                    to_port=22,
                    protocol="tcp"
                ),
                aws_lightsail.CfnInstance.PortProperty(
                    from_port=27017,
                    access_type="Public",
                    access_from="0.0.0.0/0",
                    to_port=27017,
                    protocol="tcp"
                )
            ]
        ),
        user_data=f"""
#!/bin/bash
sudo yum update -y

sudo tee /etc/yum.repos.d/mongodb-org-8.0.repo <<EOF
[mongodb-org-8.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2023/mongodb-org/8.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://pgp.mongodb.com/server-8.0.asc
EOF

sudo yum install -y mongodb-org aws-cli jq
sudo systemctl daemon-reload
sudo systemctl start mongod
sudo systemctl enable mongod
sudo systemctl status mongod
sudo chkconfig mongod on
sleep 20

mongosh <<EOF
use buzzy_bee_db;
db.createUser({{
user: '{username}',
pwd: '{password}',
roles: [
{{ role: 'readWrite', db: 'buzzy_bee_db' }},
]
}})
EOF


sudo sed -i 's/bindIp: 127.0.0.1/bindIp: 0.0.0.0/' /etc/mongod.conf
sudo systemctl restart mongod
        """

    )

    static_ip = aws_lightsail.CfnStaticIp(
        scope,
        "MongoDBStaticIpPublic",
        static_ip_name="MongoDBStaticIpPublic",
        attached_to=instance.ref
    )

    # Secure the MongoDB instance to only be accessed from the VPC
    # instance.connections.allow_from(vpc, aws_ec2.Port.tcp(27017))

    #Print out connection string
    connection_string = f"mongodb://{username}:{password}@{instance.attr_public_ip_address}/buzzy_bee_db_prod"
    CfnOutput(scope, "MongoDBConnectionString", value=connection_string)

    return connection_string, instance