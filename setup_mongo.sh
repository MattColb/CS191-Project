#!/bin/bash

sudo dnf update -y

# MongoDB repository configuration
sudo bash -c 'cat << EOF > /etc/yum.repos.d/mongodb-org-7.0.repo
[mongodb-org-7.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2023/mongodb-org/7.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-7.0.asc
EOF'

# MongoDB installation
sudo yum install mongodb-mongosh-shared-openssl3 -y
sudo yum install mongodb-mongosh -y
# sudo dnf install mongodb-org -y
sudo yum install mongodb-org-database mongodb-org-database-tools-extra -y

# MongoDB service management
sudo systemctl start mongod
sudo systemctl daemon-reload
sudo systemctl enable mongod
sudo systemctl stop mongod
sudo systemctl restart mongod

# Secure MongoDB with username and password
mongosh admin --eval 'db.createUser({user: <username>, pwd: <password>, roles: ["root"]})'
sudo sysctl -w vm.max_map_count=65530
# Check if the lines already exist in /etc/mongod.conf
sudo systemctl daemon-reload
# Configure MongoDB to require authentication in /etc/mongod.conf file
# Add security configuration to /etc/mongod.conf
echo "security:" | sudo tee -a /etc/mongod.conf
echo "    authorization: enabled" | sudo tee -a /etc/mongod.conf
sudo systemctl restart mongod

SERVERIP=$(hostname -I | awk '{print $1}')
# Set the SERVERIP environment variable
echo "export SERVERIP=$SERVERIP" | sudo tee -a /etc/environment

if grep -q "net:" /etc/mongod.conf && grep -q "bindIp:" /etc/mongod.conf; then
    # Lines exist, replace the existing bindIp value
    sudo sed -i "s/^\(\s*bindIp:\).*/\1 127.0.0.1, $SERVERIP" /etc/mongod.conf
else
    # Lines do not exist, append them to the end of the file
    echo "net:" | sudo tee -a /etc/mongod.conf
    echo "  port: 27017" | sudo tee -a /etc/mongod.conf
    echo "  bindIp: 127.0.0.1, $SERVERIP" | sudo tee -a /etc/mongod.conf
fi

sudo systemctl restart mongod