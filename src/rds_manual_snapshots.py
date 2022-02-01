import boto3

# create RDS client
rds = boto3.client('rds')

def create_rds_list():
    list_of_dbs = []
    dbs = rds.describe_db_instances()['DBInstances']
    for db in dbs:
        list_of_dbs.append(db['DBInstanceIdentifier'])
    return list_of_dbs

def create_rds_snapshot(dbs):
    for db in dbs:
        rds.create_db_snapshot(DBSnapshotIdentifier=db+'-snapshot', DBInstanceIdentifier=db)
        print("Creating snapshot for " + db)

def main():
    dbs = create_rds_list()
    create_rds_snapshot(dbs)

if __name__ == "__main__":
    main()