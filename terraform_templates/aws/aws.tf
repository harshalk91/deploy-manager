variable "ami" {}
variable "instance_count" {}
variable "instance_type" {}
variable "aws_region" {}
variable "key_name" {}
variable "subnet_id" {}
variable "security_group_id" {}
variable "instance_name" {}
variable "aws_access_key" {}
variable "aws_secret_key" {}

provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  region = var.aws_region
}

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