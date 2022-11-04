terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

}
resource "aws_instance" "evilgophish" {
  ami                  = data.aws_ami.ubuntu.id
  instance_type        = "t2.micro"
  iam_instance_profile = "rt-docker-s3-access"
  key_name             = "EvilGinx"
  security_groups      = ["Evilginx-SG"]
  user_data            = <<-EOL
  #!/bin/bash -xe

  apt-get update
  apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
  mkdir -p /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

  echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
  apt-get update
  apt-get install python3 docker-ce docker-ce-cli containerd.io docker-compose-plugin awscli --yes

  aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 758167305575.dkr.ecr.us-east-1.amazonaws.com
  docker pull 758167305575.dkr.ecr.us-east-1.amazonaws.com/mw-rt-v1:evilgophish

  docker create --name evilgophish -p80:80 -p443:443 -p3333:3333 758167305575.dkr.ecr.us-east-1.amazonaws.com/mw-rt-v1:evilgophish

  EOL

  tags = {
    Name = "EvilGoPhish"
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