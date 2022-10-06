output "evilginx.ip" {
  value = "${aws_instance.evilginx2.public_ip}"
}

output "gophish.ip" {
  value = "${aws_instance.gophish.public_ip}"
}