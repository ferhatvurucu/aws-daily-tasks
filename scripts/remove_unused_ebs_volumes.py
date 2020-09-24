import boto3

# create EC2 client
ec2 = boto3.client('ec2')

def create_volume_list():
    list_of_volumes = []
    volumes = ec2.describe_volumes(Filters=[{'Name': 'status','Values': ['available']}])
    for volume in volumes["Volumes"]:
        list_of_volumes.append(volume["VolumeId"])
    return list_of_volumes

def remove_unused_volumes(volumes):
    for volume_id in volumes:
        ec2.delete_volume(VolumeId=volume_id)
        print("Successfully deleted " + volume_id)

unused_volumes = create_volume_list()
remove_unused_volumes(unused_volumes)