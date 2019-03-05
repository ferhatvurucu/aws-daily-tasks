# daily-tasks-with-python-boto3
**AWS Key Rotation**

There is a security requirement to rotate access keys in each 90 days. Key rotation script checks each access keys and rotate them if they are created more than 90 days ago.

**EC2 Start / Stop instances**

This script helps creating a list of instances in your AWS infrastructure and schedule starting and closing the instances.

usage: ec2_start_stop.py [-h] action
