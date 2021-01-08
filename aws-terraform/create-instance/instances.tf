resource "aws_instance" "elasticsearch_instance" {
  count = var.instance_count
  ami = var.ami
  instance_type = var.instance_type
  key_name = var.key_name
  subnet_id = var.subnet_id
  associate_public_ip_address = true
  vpc_security_group_ids = var.security_group_id
  tags = {
    Name = "${var.instance_name}-Node-${count.index + 1}"
    type = "elastic"
  }
}
