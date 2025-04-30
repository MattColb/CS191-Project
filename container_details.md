aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 975049886559.dkr.ecr.us-east-1.amazonaws.com

docker tag 2d1b4bb67ff3 975049886559.dkr.ecr.us-east-1.amazonaws.com/buzzy_bee_updates:v1

docker push 975049886559.dkr.ecr.us-east-1.amazonaws.com/buzzy_bee_updates:v1