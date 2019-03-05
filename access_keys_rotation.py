import boto3
from botocore.exceptions import ClientError
import datetime

# create IAM client
iam = boto3.client('iam')

# define current date
currentDate = datetime.date.today()

def create_user_list():
    listOfUsers = []
    users = iam.list_users()
    for user in users['Users']:
        listOfUsers.append(user['UserName'])    
    return listOfUsers

def deactive_old_key(userName,accessKey):
    iam.update_access_key(AccessKeyId=accessKey,Status='Inactive',UserName=userName)
    print('Successfully deactived key for the user ' + userName)

def create_new_key(userName):
    try:
        response=iam.create_access_key(UserName=userName)
        accessKey=response['AccessKey']
        print('Username: ' + userName + '\nAccessKey: ' + str(accessKey['AccessKeyId']) + '\nSecretAccessKey: ' + str(accessKey['SecretAccessKey']))
    except ClientError as e:
        print(e)

def rotate_keys_for_users(listOfUsers):
    for user in listOfUsers:
        keys = iam.list_access_keys(UserName=user)
        for key in keys['AccessKeyMetadata']:
            creationDate=key['CreateDate']
            accessKey=key['AccessKeyId']
            keyStatus=key['Status']
            if (currentDate - creationDate.date()).days > 90 and keyStatus == 'Active':
                deactive_old_key(user,accessKey)
                create_new_key(user)
            elif keyStatus == 'Inactive':
                print(user + ' access key is inactive.')
            else:
                print(user + ' access key is active for less then 90 days.')

userList = create_user_list()
rotate_keys_for_users(userList)