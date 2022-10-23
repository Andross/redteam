terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

}
resource "aws_instance" "evilginx2" {
  ami                  = data.aws_ami.evilginx2_ami.id
  instance_type        = "t2.micro"
  iam_instance_profile = "mwrt-s3-role"
  key_name             = "EvilGinx"
  security_groups      = ["Evilginx-SG"]
  # user_data = <<-EOL
  # #!/bin/bash -xe

  # apt install apache2
  # a2enmod ssl rewrite proxy proxy_http
  # rm 000-default.conf
  # ln -s /etc/apache2/sites-available/default-ssl.conf /etc/apache2/sits-enabled/

  # EOL


  tags = {
    Name = "EvilGinx2"
  }
}

# resource "aws_instance" "gophish" {
#   ami                  = data.aws_ami.gophish_ami.id
#   instance_type        = "t2.micro"
#   iam_instance_profile = "mwrt-s3-role"
#   key_name             = "GoPhish"
#   security_groups      = ["GoPhish-SG"]
#   # user_data = <<-EOL
#   # #!/bin/bash -xe

#   # apt install apache2
#   # a2enmod ssl rewrite proxy proxy_http
#   # rm 000-default.conf
#   # ln -s /etc/apache2/sites-available/default-ssl.conf /etc/apache2/sits-enabled/

#   # EOL


#   tags = {
#     Name = "GoPhish"
#   }
# }

# data "aws_ami" "gophish_ami" {
#   most_recent = true
#   owners      = ["self"]
#   filter {
#     name   = "name"
#     values = ["GoPhish AMI"]
#   }

# }


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

  aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 758167305575.dkr.ecr.us-east-1.amazonaws.com
  docker pull 758167305575.dkr.ecr.us-east-1.amazonaws.com/mw-rt-v1:redirector

  docker create --name redirector -p443:443 -p80:80 758167305575.dkr.ecr.us-east-1.amazonaws.com/mw-rt-v1:redirector

  docker start redirector

  EOL


  tags = {
    Name = "RedirectorDocker"
  }
}

resource "aws_instance" "gophish-docker" {
  ami                  = data.aws_ami.ubuntu.id
  instance_type        = "t2.micro"
  iam_instance_profile = "rt-docker-s3-access"
  key_name             = "GoPhish"
  security_groups      = ["GoPhish-SG"]
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

  aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 758167305575.dkr.ecr.us-east-1.amazonaws.com
  docker pull 758167305575.dkr.ecr.us-east-1.amazonaws.com/mw-rt-v1:gophish

  docker create --name gophish -p3333:3333 758167305575.dkr.ecr.us-east-1.amazonaws.com/mw-rt-v1:gophish

  docker start gophish

  EOL


  tags = {
    Name = "GoPhishDocker"
  }
}

data "aws_ami" "evilginx2_ami" {
  most_recent = true
  owners      = ["self"]

  filter {
    name   = "name"
    values = ["EvilGinx2 AMI"]
  }

}