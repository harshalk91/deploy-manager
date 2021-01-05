module "create-instance" {
  source = "./create-instance"
  ami = var.ami
  instance_type = var.instance_type
  subnet_id = var.subnet_id
  key_name = var.key_name
  aws_region = var.aws_region
  instance_count = var.instance_count
  security_group_id = var.security_group_id
  instance_name = var.instance_name
}
