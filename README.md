# AWS EC2 Instance Deployment and K3s Installation Using Pulumi (Python)
I have explained the below steps to deploy the EC2 instance and installed k3s on EC2 instance using Pulumi with Python

## Prerequisites
- AWS CLI configured with appropriate credentials
- Pulumi CLI installed.
- Python
- A valid EC2 Key Pair already created in AWS (e.g., mykey and mykey.pem)

## Pulumi Stack Explanation
- Security Group: Custom SG allowing SSH, HTTP, HTTPS, and NodePort range access (Enable some standard ports, incase need to expose application using NodePort)
- EC2 Instance: Ubuntu-based EC2 (t2.micro) launched with the above configurations
- Remote Command: Utilized remote command to install k3s using a simple curl and sh command

## Code Workdlow
- Import Pulumi libraries (pulumi, pulumi_aws, pulumi_command)
- Create Security Group with required ingress and egress rules
- Launch EC2 Instance with:
  - Ubuntu AMI (ami-0e35ddab05955cf57)
  - SSH key (mykey)
  - Attached Security Group
  - Deployed in the selected subnet
- Install k3s remotely using the pulumi_command.remote.Command resource:
  - SSH into the instance using the private key (mykey.pem).
  - Execute: curl -sfL https://get.k3s.io | sh - to install k3s
- Export outputs like instance ID, public IP, VPC ID, Subnet ID, and Security Group ID

