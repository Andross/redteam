output "evilginx_ip" {
  value = aws_instance.evilginx2.public_ip
}

output "gophish_ip" {
  value = aws_instance.gophish.public_ip
}