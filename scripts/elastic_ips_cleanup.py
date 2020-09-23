import boto3

# create EC2 client
ec2 = boto3.client('ec2')

def elastic_ip_cleanup():
    elastic_ips = ec2.describe_addresses()
    for eip in elastic_ips['Addresses']:
        if "InstanceId" not in eip:
            ec2.release_address(AllocationId=eip['AllocationId'])
            print("Released " + eip['PublicIp'])

elastic_ip_cleanup()