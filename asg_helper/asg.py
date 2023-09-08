import boto3
import os
from typing import List, Dict, Union, Optional
import datetime

class ASGHelper:
    def __init__(self, region: str, access_key: str, secret_key: str):
        """
        Initialize ASGHelper with AWS region and credentials.

        Args:
            region (str): The AWS region where the ASG is located.
            access_key (str): The AWS access key.
            secret_key (str): The AWS secret key.
        """
        self.region = os.getenv('AWS_REGION')
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.client = boto3.client('autoscaling', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)
        self.asg_name = self.get_asg_name()  # Fetch ASG name dynamically

    def get_asg_name(self) -> Optional[str]:
        """
        Fetch the Auto Scaling Group (ASG) name based on criteria.

        Returns:
            Optional[str]: The ASG name if found, else None.
        """
        # Implement logic to fetch the ASG name dynamically
        # You can list ASGs and select one based on your criteria
        # For this example, let's fetch the first ASG we find
        response = self.client.describe_auto_scaling_groups()
        if 'AutoScalingGroups' in response and response['AutoScalingGroups']:
            return response['AutoScalingGroups'][0]['AutoScalingGroupName']
        else:
            return None
        
    def get_asg_instances(self) -> List[Dict[str, Union[str, datetime.datetime]]]:
        """
        Get the instances associated with the Auto Scaling Group (ASG).

        Returns:
            List[Dict[str, Union[str, datetime.datetime]]]: A list of instances with their details.
        """
        response = self.client.describe_auto_scaling_instances()
        print(response)
        return response['AutoScalingInstances']


    def validate_asg_running_count(self) -> bool:
        """
        Validate that the desired running count matches the running instances count in the ASG.

        Returns:
            bool: True if the validation passes, False otherwise.
        """
        instances = self.get_asg_instances()
        desired_count = len(instances)
        running_count = sum(1 for instance in instances if instance['LifecycleState'] == 'InService')
        return desired_count == running_count

    def validate_az_distribution(self) -> bool:
        """
        Validate that if more than one instance is running, they are distributed across multiple availability zones.

        Returns:
            bool: True if the validation passes, False otherwise.
        """
        instances = self.get_asg_instances()
        if len(instances) > 1:
            az_set = set(instance['AvailabilityZone'] for instance in instances)
            return len(az_set) > 1
        else:
            return True
    
    


    def validate_instance_properties(self) -> bool:
        """
        Validate that SecurityGroup, ImageID, and VPCID are the same for all running instances in the ASG.

        Returns:
            bool: True if the validation passes, False otherwise.
        """

        instances = self.get_asg_instances()
        print(instances)
        for instance in instances:
            # Add logging to print instance properties for debugging
            print(f"Instance ID: {instance['InstanceId']}")
            print(f"SecurityGroup: {instance['SecurityGroups']}")
            print(f"ImageID: {instance['ImageId']}")
            print(f"VPCID: {instance['VpcId']}")
        if instances:
            reference_instance = instances[0]
            for instance in instances:
                if (
                    instance['SecurityGroups'] != reference_instance['SecurityGroups'] or
                    instance['ImageId'] != reference_instance['ImageId'] or
                    instance['VpcId'] != reference_instance['VpcId']
                ):
                    return False
            return True
        else:
            return False

    def get_longest_running_instance_uptime(self) -> Optional[datetime.timedelta]:
        """
        Get the uptime of the longest-running instance in the ASG.

        Returns:
            Optional[datetime.timedelta]: The uptime of the longest-running instance if found, else None.
        """
        instances = self.get_asg_instances()
        if instances:
            now = datetime.datetime.now(datetime.timezone.utc)
            longest_running_instance = max(instances, key=lambda x: now - x['LaunchTime'])
            uptime = now - longest_running_instance['LaunchTime']
            return uptime

    def get_scheduled_actions(self) -> List[Dict[str, Union[str, datetime.datetime]]]:
        """
        Get the scheduled actions for the ASG.

        Returns:
            List[Dict[str, Union[str, datetime.datetime]]]: A list of scheduled actions with their details.
        """
        response = self.client.describe_scheduled_actions(AutoScalingGroupName=self.asg_name)
        return response['ScheduledUpdateGroupActions']

    def calculate_elapsed_time(self, scheduled_actions: List[Dict[str, Union[str, datetime.datetime]]]) -> Optional[datetime.timedelta]:
        """
        Calculate the elapsed time until the next scheduled action.

        Args:
            scheduled_actions (List[Dict[str, Union[str, datetime.datetime]]]): List of scheduled actions.

        Returns:
            Optional[datetime.timedelta]: The elapsed time until the next scheduled action if found, else None.
        """
        now = datetime.datetime.now(datetime.timezone.utc)
        next_action_time = min(action['StartTime'] for action in scheduled_actions)
        elapsed_time = next_action_time - now
        return elapsed_time

    def get_instances_launched_terminated_today(self) -> List[Dict[str, Union[str, datetime.datetime]]]:
        """
        Get instances launched or terminated today for the ASG.

        Returns:
            List[Dict[str, Union[str, datetime.datetime]]]: A list of instances launched or terminated today with their details.
        """
        today = datetime.date.today()
        start_time = datetime.datetime.combine(today, datetime.time.min, tzinfo=datetime.timezone.utc)
        end_time = datetime.datetime.combine(today, datetime.time.max, tzinfo=datetime.timezone.utc)
        response = self.client.describe_scaling_activities(
            AutoScalingGroupName=self.asg_name,
            StartTime=start_time,
            EndTime=end_time
        )
        return response['Activities']

