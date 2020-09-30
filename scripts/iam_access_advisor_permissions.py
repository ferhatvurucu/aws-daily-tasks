import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timezone

# create IAM client
iam = boto3.client('iam')

def list_roles():
    list_of_roles = []
    roles = iam.list_roles()
    for role in roles['Roles']:
        list_of_roles.append(role['Arn'])
    return list_of_roles

def access_advisor_permissions(role_arn):
    current_time = datetime.now(timezone.utc)
    # returns job id
    job_id_response = iam.generate_service_last_accessed_details(Arn=role_arn)
    role_job_id = job_id_response['JobId']
    # returns service last accessed details
    service_response = iam.get_service_last_accessed_details(JobId=role_job_id)
    while service_response['JobStatus'] != 'COMPLETED':
      service_response = iam.get_service_last_accessed_details(JobId=role_job_id)
    # getting last accessed services
    last_accessed_services = service_response['ServicesLastAccessed']
    print('- - - Role: ' + role_arn.split("/")[-1] + ' - - -')
    for service in last_accessed_services:
        try:
            last_access_day = service['LastAuthenticated']
            days_difference = int((current_time - last_access_day).days)
            # iam roles with services older than 180 days
            if days_difference > 180:
                print(f"{service['ServiceName']} - Last accessed {days_difference} days ago.")
        except Exception as e:
            continue

def main():
    role_arns = list_roles()
    for role_arn in role_arns:
        access_advisor_permissions(role_arn)

if __name__ == "__main__":
    main()