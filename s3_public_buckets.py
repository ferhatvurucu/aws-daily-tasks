import boto3
from botocore.exceptions import ClientError

# create S3 client
s3 = boto3.client('s3')

def public_access_block_status(bucket):
    try:
        response = s3.get_public_access_block(Bucket=bucket)
        if not (response['PublicAccessBlockConfiguration']['BlockPublicAcls'] and response['PublicAccessBlockConfiguration']['BlockPublicPolicy']):
            return True
    except ClientError as e:
        # no valid public access block configuration
        return True

def bucket_policy_status(bucket):
    try:
        response = s3.get_bucket_policy_status(Bucket=bucket)
        if response['PolicyStatus']['IsPublic']:
            return True
    except ClientError:
        # no valid ACL
        return False

def bucket_acl_status(bucket):
    response = s3.get_bucket_acl(Bucket=bucket)['Grants']
    for grantee in response:
        if grantee['Grantee']['Type'] == "Group" and (grantee['Grantee']['URI'] == "http://acs.amazonaws.com/groups/global/AuthenticatedUsers" or grantee['Grantee']['URI'] == "http://acs.amazonaws.com/groups/global/AllUsers"):
            return True
            break

def list_public_buckets():
    buckets = s3.list_buckets()['Buckets']
    for bucket in buckets:
        if not public_access_block_status(bucket['Name']):
            continue
        elif bucket_policy_status(bucket['Name']) or bucket_acl_status(bucket['Name']):
            print(bucket['Name'] + ' is public.')

list_public_buckets()