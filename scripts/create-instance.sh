#!/bin/bash
echo "================================"
echo "Terraform Initialization Started"
cd $1
terraform init
echo "Terraform Initialization Complete"
echo "================================"
echo "Triggering Terraform Instance Creation Script"
terraform plan -target=module.create-instance
echo "Terraform Plan Complete"
terraform apply -target=module.create-instance -auto-approve
