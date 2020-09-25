import boto3
from botocore.exceptions import ClientError

# create IAM client
iam = boto3.client('iam')

def users_without_mfa():
    list_of_users = []
    users = iam.list_users()
    for user in users['Users']:
        response = iam.list_mfa_devices(UserName=user['UserName'])
        if not response['MFADevices']:
            list_of_users.append(user['UserName'])
    return list_of_users

def disable_console_access(userlist):
    for user in userlist:
        try:
            iam.delete_login_profile(UserName=user)
            print("Deleted the password for " + user)
        except:
            print("There is no login profile for " + user)
            continue

userlist = users_without_mfa()
disable_console_access(userlist)