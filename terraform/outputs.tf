output "evilginx_ip" {
  value = aws_instance.evilginx2.public_ip
}

output "gophish-docker_ip" {
  value = aws_instance.gophish-docker.public_ip
}

output "redirector_ip" {
  value = aws_instance.redirector-docker.public_ip
}