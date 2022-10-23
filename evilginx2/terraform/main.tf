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