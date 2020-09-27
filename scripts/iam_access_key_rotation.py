import boto3
from botocore.exceptions import ClientError
import datetime

# create IAM client
iam = boto3.client('iam')

# define current date
current_date = datetime.date.today()

def create_user_list():
    list_of_users = []
    users = iam.list_users()
    for user in users['Users']:
        list_of_users.append(user['UserName'])    
    return list_of_users

def deactive_old_key(username,accesskey):
    iam.update_access_key(AccessKeyId=accesskey,Status='Inactive',UserName=username)
    print('Successfully deactived key for the user ' + username)

def create_new_key(username):
    try:
        response=iam.create_access_key(UserName=username)
        accesskey=response['AccessKey']
        print('Username: ' + username + '\nAccessKey: ' + str(accesskey['AccessKeyId']) + '\nSecretAccessKey: ' + str(accesskey['SecretAccessKey']))
    except ClientError as e:
        print(e)

def rotate_keys_for_users(list_of_users):
    for user in list_of_users:
        keys = iam.list_access_keys(UserName=user)
        for key in keys['AccessKeyMetadata']:
            creation_date=key['CreateDate']
            accesskey=key['AccessKeyId']
            keystatus=key['Status']
            if (current_date - creation_date.date()).days > 90 and keystatus == 'Active':
                deactive_old_key(user,accesskey)
                create_new_key(user)
            elif keystatus == 'Inactive':
                print(user + ' access key is inactive.')
            else:
                print(user + ' access key is active for less then 90 days.')

def main():
    user_list = create_user_list()
    rotate_keys_for_users(user_list)

if __name__ == "__main__":
    main()