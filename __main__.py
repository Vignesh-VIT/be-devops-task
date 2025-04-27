"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
import pulumi_command as command 

default_vpc = aws.ec2.get_vpc(default=True)

default_subnets = aws.ec2.get_subnets(filters=[
    {"name": "vpc-id", "values": [default_vpc.id]},
])

first_subnet_id = default_subnets.ids[0]

custom_sg = aws.ec2.SecurityGroup("be-custom-sg",
    description="Allow HTTP, HTTPS, SSH and custom TCP ports",
    vpc_id=default_vpc.id,
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=22,
            to_port=22,
            cidr_blocks=["0.0.0.0/0"],
            description="Allow SSH",
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=80,
            to_port=80,
            cidr_blocks=["0.0.0.0/0"],
            description="Allow HTTP",
        ),
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=443,
            to_port=443,
            cidr_blocks=["0.0.0.0/0"],
            description="Allow HTTPS",
        ),
        # Allow custom TCP range (NodePort). Incase, if we want to access the application outside.
        aws.ec2.SecurityGroupIngressArgs(
            protocol="tcp",
            from_port=30000,
            to_port=32767,
            cidr_blocks=["0.0.0.0/0"],
            description="Allow NodePort Range",
        ),
    ],
    egress=[
        aws.ec2.SecurityGroupEgressArgs(
            protocol="-1",
            from_port=0,
            to_port=0,
            cidr_blocks=["0.0.0.0/0"],
            description="Allow all outbound traffic",
        ),
    ],
    tags={
        "Name": "be-custom-sg",
    },
)

ec2_instance = aws.ec2.Instance('k3s-setup',
                                ami="ami-0e35ddab05955cf57",
                                instance_type="t2.micro",
                                key_name="mykey",
                                subnet_id=first_subnet_id,
                                vpc_security_group_ids=[custom_sg.id],
                                tags={"Name": "k3s_instance", "Owner": "vignesh", "Task": "be-devops-task"}
                            )


install_k3s = command.remote.Command("install-k3s",
    connection=command.remote.ConnectionArgs(
        host=ec2_instance.public_ip,
        user="ubuntu",
        private_key=pulumi.Output.secret(open("mykey.pem").read()), 
    ),
    create="curl -sfL https://get.k3s.io | sh -", 
)

pulumi.export("instance_id", ec2_instance.id)
pulumi.export("public_ip", ec2_instance.public_ip)
pulumi.export("default_vpc_id", default_vpc.id)
pulumi.export("default_subnet_id", first_subnet_id)
pulumi.export("default_security_group_id", custom_sg.id)