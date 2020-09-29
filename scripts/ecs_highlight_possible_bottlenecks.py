import boto3
import datetime
import os
from termcolor import colored

# create ecs and cloudwatch client
ecs = boto3.client("ecs")
cloudwatch = boto3.client("cloudwatch")

def list_clusters():
    list_of_clusters = []
    cluster_arns = ecs.list_clusters()
    for arn in cluster_arns['clusterArns']:
        list_of_clusters.append(arn)
    return list_of_clusters

def list_services(cluster_name):
    list_of_services = []
    service_arns = ecs.list_services(cluster=cluster_name,maxResults=100)
    for service in service_arns['serviceArns']:
        list_of_services.append(service)
    return list_of_services

def get_max_utilization(cluster_name, service_name, start_time, end_time, metric_name):
    response = cloudwatch.get_metric_statistics(
        Namespace="AWS/ECS",
        MetricName=metric_name,
        Dimensions=[
            {"Name": "ClusterName", "Value": cluster_name},
            {"Name": "ServiceName", "Value": service_name},
        ],
        StartTime=start_time,        
        EndTime=end_time,
        Period=3600,
        Statistics=["Maximum"]
    )

    try:
        return max(datapoint["Maximum"] for datapoint in response["Datapoints"])
    except ValueError:
        return 0.0

def highlight_bottlenecks(data):
    for service, value in data:
            line = service + " | " + "{:.1f}%".format(value)
            if value > 80:
                print(colored(line, 'red'))
            else:
                print(colored(line, 'green'))

def main():
    list_of_clusters = list_clusters()
    for cluster in list_of_clusters:
        # cluster arn
        cluster_arn = cluster
        # cpu and memory stats
        cpu_stats = []
        memory_stats = []
        # cluster name
        cluster_name = cluster_arn.split("/")[-1]
        # last 24 hours
        now = datetime.datetime.now()
        start_time = now - datetime.timedelta(hours=24)
        # service arn
        list_of_services = list_services(cluster_name)
        # print cluster name
        print("Cluster: " + cluster_name)

        for service_arn in list_of_services:
            service_name = service_arn.split("/")[-1]
            # get max cpu utilization
            max_cpu = get_max_utilization(cluster_name, service_name , start_time, now, metric_name= "CPUUtilization")
            cpu_stats.append((service_name, max_cpu))
            # get max memory utilization
            max_memory = get_max_utilization(cluster_name, service_name , start_time, now, metric_name= "MemoryUtilization")
            memory_stats.append((service_name, max_memory))
                
        print("\n--- CPU Utilization ---\n")
        highlight_bottlenecks(cpu_stats)

        print("\n--- Memory Utilization ---\n")
        highlight_bottlenecks(memory_stats)

if __name__ == "__main__":
    main()