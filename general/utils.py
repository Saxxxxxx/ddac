from django.db import models
from account.models import User

import uuid
import boto3

class AuditInfoDeleted(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="%(class)s_created_by_user")
    date_created = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="%(class)s_changed_by_user")
    date_changed = models.DateTimeField(blank=True, null=True)
    deleted = models.BooleanField(blank=True, null=True, default=False)
    deleted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="%(class)s_retired_by_user")
    date_deleted = models.DateTimeField(blank=True, null=True)
    delete_reason = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

class Utilities():
    def generate_uuid():
        return str(uuid.uuid4())


class SNSUtilities:
    def __init__(self, region_name, aws_access_key_id, aws_secret_access_key, aws_session_token=None):
        self.region_name = region_name
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_session_token = aws_session_token
        
        # Initialize SNS client
        self.sns_client = boto3.client(
            'sns',
            region_name=self.region_name,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            aws_session_token=self.aws_session_token
        )
    
    def send_notification(self, message, subject, topic_arn):
        """
        Send a notification to the specified SNS topic.
        
        Args:
            message (str): The message content.
            subject (str): The subject of the notification.
            topic_arn (str): The ARN of the SNS topic.
        
        Returns:
            str: The message ID of the published message.
        """
        response = self.sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
        # return response['MessageId']
    def subscribe_user_to_sns(self, email, topic_arn):
        """
        Subscribe a user's email to the specified SNS topic.
        
        Args:
            user (User): The user object with an email address.
            topic_arn (str): The ARN of the SNS topic.
        
        Returns:
            dict: The response from the subscribe operation.
        """
        # Check if the user has an email address
        if email:
            # Subscribe user's email to the SNS topic
            response = self.sns_client.subscribe(
                TopicArn=topic_arn,
                Protocol='email',
                Endpoint=email
            )
    
    def get_list_of_subscriber(self, topic_arn):
        """
        List all subscriptions for a given topic.
        
        Args:
            topic_arn (str): The ARN of the SNS topic.
        
        Returns:
            list: A list of subscription ARNs.
        """
        # List subscriptions by topic
        response = self.sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
        subscriptions = response['Subscriptions']
        return subscriptions
    def filter_subscriptions_by_email(self, subscriptions, email):
        """
        Filter subscriptions by email address.
        
        Args:
            subscriptions (list): A list of subscription details.
            email (str): The email address to filter subscriptions by.
        
        Returns:
            list: A list of filtered subscription details.
        """
        return [sub for sub in subscriptions if sub['Protocol'] == 'email' and sub['Endpoint'] == email]

    def unsubscribe_endpoints_by_email(self,filtered_subscriptions):
        # Unsubscribe endpoints
        print(filtered_subscriptions)
        for subscription in filtered_subscriptions:
            self.sns_client.unsubscribe(SubscriptionArn=subscription['SubscriptionArn'])
            print("Unsubscribed from:", subscription['SubscriptionArn'])