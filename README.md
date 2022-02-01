# aws-daily-tasks

A collection of scripts to automate AWS day-to-day activities with Boto3.

# Usage

Name    |  Description |
-----   | -------------
[IAM Access Key Rotation](src/iam_access_key_rotation.py) | Lists access keys older than 90 days and helps you to rotate them |
[EC2 Start / Stop instances](src/ec2_start_stop.py) | Lists EC2 instances and helps you to start and stop them all at once <br /> usage: ec2_start_stop.py [-h] [--start] [--stop]  |
[Remove Unused EBS Volumes](src/remove_unused_ebs_volumes.py) | Lists unused Amazon EBS volumes and helps you to control AWS costs by deleting them |
[RDS Untagged Resources](src/rds_untagged_resources.py) | Lists untagged RDS resources and helps you to identify them |
[Public S3 Buckets](src/public_s3_buckets.py) | Lists public S3 buckets by evaluating Bucket Policy, Access Control List and Block Public Access settings |
[Elastic IP Clean Up](src/elastic_ips_cleanup.py) | Lists unused Elastic IPs and helps you to stop the charges by releasing them |
[RDS Manual Snapshots](src/rds_manual_snapshots.py) | Lists RDS instances and helps you to have manual snapshots all at once |
[Disable IAM Users Without MFA](src/disable_iam_users_without_mfa.py) | Lists all users without MFA enabled and helps you to terminate the user's ability to access AWS services |
[AWS Parameter Store Backup / Restore](src/parameter_store_backup_restore.py) | Lists all parameters and helps you to backup and restore sensitive data all at once <br /> usage: parameter_store_backup_restore.py [-h] [-b] [-r] |
[Amazon Translate Large Text Documents](src/translate_large_text_documents.py) | Helps you to translate large text documents with Amazon Translate and Natural Language Toolkit for Python <br /> usage: translate_large_text_documents.py [-h] -l LANG |
[AWS ECS Highlight Possible Bottlenecks](src/ecs_highlight_possible_bottlenecks.py) | Helps you to summarize CPU and memory usages across an ECS cluster over the last 24 hours |
[IAM Access Advisor Permissions Analysis](src/iam_access_advisor_permissions.py) | Helps you to audit IAM roles by listing services not accessed for the last 180 days |

# References

- [Boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
