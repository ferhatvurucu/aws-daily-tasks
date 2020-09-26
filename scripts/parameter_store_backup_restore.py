import boto3
import json
from argparse import ArgumentParser
from botocore.exceptions import ClientError

ssm = boto3.client('ssm')

backup_file = 'ssm_backup.json'

# argument parser for backup / restore action
parser = ArgumentParser(description='Backup or restore Systems Manager Parameter Store')
parser.add_argument('-b', '--backup', action='store_true', help="parameter store backup")
parser.add_argument('-r', '--restore', action='store_true', help="parameter store restore")
args = parser.parse_args()

def backup():
    ssm_data = dict()
    parameters = ssm.describe_parameters()['Parameters']
    
    for param in parameters:
        response = ssm.get_parameter(Name=param['Name'], WithDecryption=True)
        ssm_data[param['Name']] = response['Parameter']['Value']
    
    with open(backup_file, 'w') as json_file:
        json.dump(ssm_data, json_file)
    
    print("Successfully saved " + backup_file)

def restore():
    try:
        with open(backup_file, 'r') as message_json:
            ssm_data = json.load(message_json)
        
        for k,v in ssm_data.items():
            ssm.put_parameter(Name=k,Value=v,Type='SecureString')

        print("Successfully restored " + backup_file)
    
    except (ClientError,IOError) as e:
        print(e)

def main():
    if args.backup:
        backup()
    elif args.restore:
        restore()
    else:
        print("usage: parameter_store_backup_restore.py [-h] [-b] [-r]")

if __name__ == "__main__":
    main()