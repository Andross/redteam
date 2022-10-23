output "gophish-docker_ip" {
  value = aws_instance.gophish-docker.public_ip
}