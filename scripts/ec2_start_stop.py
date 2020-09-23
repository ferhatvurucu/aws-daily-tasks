import boto3
from argparse import ArgumentParser
from botocore.exceptions import ClientError

# argument parser for start/stop action
parser = ArgumentParser(description='Start or stop EC2 instances')
parser.add_argument('action',help='start / stop',type=str)
args = parser.parse_args()
action=(args.action).upper()

# create EC2 resource and client
ec2_resource = boto3.resource('ec2')
ec2_client = boto3.client('ec2')

def create_ec2_list():
    list_of_instances=[]
    for instance in ec2_resource.instances.all():
        list_of_instances.append(str(instance.id))
        return list_of_instances

def start_instances(instances):
    try:
        for id in instances:
            ec2_client.start_instances(InstanceIds=[id], DryRun=False)
            print(id + ' has been started.')
    except ClientError as e:
        print(e)

def stop_instances(instances):
    try:
        for id in instances:
            ec2_client.stop_instances(InstanceIds=[id], DryRun=False)
            print(id + ' has been stopped.')
    except ClientError as e:
        print(e)

instance_list = create_ec2_list()

if action == 'START':
    start_instances(instance_list)
elif action == 'STOP':
    stop_instances(instance_list)
else:
    print('usage: ec2_start_stop.py [-h] action')