import boto3

# create RDS client
rds = boto3.client('rds')

def list_untagged_dbs():
    databases = rds.describe_db_instances()['DBInstances']
    for db in databases:
        if not rds.list_tags_for_resource(ResourceName=db['DBInstanceArn'])['TagList']:
            print("DB Identifier : " + db['DBInstanceIdentifier'])

def main():
    list_untagged_dbs()

if __name__ == "__main__":
    main()