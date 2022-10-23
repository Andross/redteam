terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

}


resource "aws_instance" "redirector-docker" {
  ami                  = data.aws_ami.ubuntu.id
  instance_type        = "t2.micro"
  iam_instance_profile = "rt-docker-s3-access"
  key_name             = "Redirector"
  security_groups      = ["Redirector-SG"]
  user_data            = <<-EOL
  #!/bin/bash -xe

  apt update
  apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
  mkdir -p /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  
  echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
  apt update
  apt install python3 docker-ce docker-ce-cli containerd.io docker-compose-plugin awscli --yes

  ROLENAME=$(curl http://169.254.169.254/latest/meta-data/iam/security-credentials/ -s)
  KeyURL="http://169.254.169.254/latest/meta-data/iam/security-credentials/"$ROLENAME"/"
  wget $KeyURL -q -O Iam.json
  KEYID=$(grep -Po '.*"AccessKeyId".*' Iam.json | sed 's/ //g' | sed 's/"//g' | sed 's/,//g' | sed 's/AccessKeyId://g')
  SECRETKEY=$(grep -Po '.*"SecretAccessKey".*' Iam.json | sed 's/ //g' | sed 's/"//g' | sed 's/,//g' | sed 's/SecretAccessKey://g')
  SECURITYTOKEN=$(grep -Po '.*"Token".*' Iam.json | sed 's/ //g' | sed 's/"//g' | sed 's/,//g' | sed 's/Token://g')
  rm Iam.json -f

  aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 758167305575.dkr.ecr.us-east-1.amazonaws.com
  docker pull 758167305575.dkr.ecr.us-east-1.amazonaws.com/mw-rt-v1:redirector

  docker create --name redirector -e AWS_ACCESS_KEY_ID=$KEYID -e AWS_SECRET_ACCESS_KEY=$SECRETKEY -e AWS_SESSION_TOKEN=$SECURITYTOKEN -p3333:3333 758167305575.dkr.ecr.us-east-1.amazonaws.com/mw-rt-v1:redirector 

  docker start redirector

  EOL


  tags = {
    Name = "RedirectorDocker"
  }
}


data "aws_ami" "ubuntu" {

  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"]
}