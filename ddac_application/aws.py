import json
from pathlib import Path
import requests
# from aws_requests_auth.aws_auth import AWSRequestsAuth
from requests_aws4auth import AWS4Auth
import environ
    
env = environ.Env(
    DEBUG=(bool,False)
)
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(BASE_DIR/'.env')

auth = AWS4Auth(env('AWS_ACCESS_KEY_ID'), env('AWS_SECRET_ACCESS_KEY'), 'us-east-1', 'execute-api',session_token=env('AWS_SESSION_TOKEN'))
api_url = 'https://62i9cvwa68.execute-api.us-east-1.amazonaws.com'

class S3AWS():
    def upload_s3_to_api(upload_array_data):
        upload_array_data = json.dumps(upload_array_data)
        api_url = api_url + '/upload_to_s3'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, headers=headers, data=upload_array_data,auth=auth)
        response.raise_for_status()  # Raise an exception if the API call fails

    def delete_s3_to_api(delete_array_data):
        delete_array_data = json.dumps(delete_array_data)
        api_url = api_url + '/delete_to_s3'
        headers = {'Content-Type': 'application/json'}
        response = requests.delete(api_url, headers=headers, data=delete_array_data,auth=auth)
        response.raise_for_status()  # Raise an exception if the API call fails


    def update_s3_to_api(upload_array_data, delete_array_data):
        json_data = {
            "upload_data": upload_array_data,
            "delete_data": delete_array_data
        }
        json_data = json.dumps(json_data)
        # Send the request with JSON data
        api_url = api_url + '/update_to_s3'
        headers = {'Content-Type': 'application/json'}
        response = requests.put(api_url, headers=headers, data=json_data,auth=auth)
        response.raise_for_status()  # Raise an exception if the API call fails

class SNSUtilities:
    def send_notification(message, subject, topic_arn):
        """
        Send a notification to the specified SNS topic.
        
        Args:
            message (str): The message content.
            subject (str): The subject of the notification.
            topic_arn (str): The ARN of the SNS topic.
        
        Returns:
            str: The message ID of the published message.
        """
        json_data={
            "sns_topic_arn":topic_arn,
            "message":message,
            "subject":subject
        }
        json_data = json.dumps(json_data)
        api_url = api_url + '/send_notification'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, headers=headers, data=json_data,auth=auth)
        response.raise_for_status()  # Raise an exception if the API call fails
        
    def subscribe_user_to_sns(email, topic_arn):
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
            json_data = {
                "sns_topic_arn": topic_arn,
                'endpoint':email,
                "protocol": 'email',
            }
            json_data = json.dumps(json_data)
            api_url = api_url + '/subscribe_to_sns'
            # Send the request with JSON data
            headers = {'Content-Type': 'application/json'}
            response = requests.post(api_url, headers=headers, data=json_data,auth=auth)
            response.raise_for_status()  # Raise an exception if the API call fails

    def unsubscribe_user_to_sns(email,topic_arn):
        json_data = {
            "sns_topic_arn": topic_arn,
            'email':email,
        }
        json_data = json.dumps(json_data)
        # Send the request with JSON data
        api_url = api_url + '/unsubscribe_to_sns'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(api_url, headers=headers, data=json_data,auth=auth)
        response.raise_for_status()  # Raise an exception if the API call fails