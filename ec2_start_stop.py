import boto3
from argparse import ArgumentParser
from botocore.exceptions import ClientError

# argument parser for start/stop action
parser = ArgumentParser(description='Start or stop EC2 instances')
parser.add_argument('action',help='start / stop',type=str)
args = parser.parse_args()
action=(args.action).upper()

# create EC2 resource and client
ec2Resource = boto3.resource('ec2')
ec2Client = boto3.client('ec2')

def create_ec2_list():
    listOfInstances=[]
    for instance in ec2Resource.instances.all():
        listOfInstances.append(str(instance.id))
        return listOfInstances

def start_instances(instanceList):
    try:
        for id in instanceList:
            ec2Client.start_instances(InstanceIds=[id], DryRun=False)
            print(id + ' has been started.')
    except ClientError as e:
        print(e)

def stop_instances(instanceList):
    try:
        for id in instanceList:
            ec2Client.stop_instances(InstanceIds=[id], DryRun=False)
            print(id + ' has been stopped.')
    except ClientError as e:
        print(e)

instanceList = create_ec2_list()

if action == 'START':
    start_instances(instanceList)
elif action == 'STOP':
    stop_instances(instanceList)
else:
    print('usage: ec2_start_stop.py [-h] action')