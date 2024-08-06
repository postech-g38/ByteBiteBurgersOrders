from typing import Dict, Any, Optional, List
import json

import boto3


class AwsSQS:
    def __init__(self, name: Optional[str] = None, url: Optional[str] = None) -> None:
        self._client = boto3.client('sqs')
        self._reference = name or url

    def publish(self, message: Dict[str, Any], key: Optional[str] = None) -> Dict[str, Any]:
        response = self._client.send_message(
            MessageGroupId='order',
            QueueUrl=self._reference, 
            MessageBody=json.dumps(message)
        )
        return response
    
    def consume(
        self, 
        name: str, 
        max_message: int = 5, 
        visibility_timeout_seconds: int = 20, 
        wait_seconds: int = 2
    ) -> List[Dict[str, str | bytes]]:
        response = self._client.receive_message(
            QueueUrl=name,
            MaxNumberOfMessages=max_message,
            VisibilityTimeout=visibility_timeout_seconds,
            WaitTimeSeconds=wait_seconds,
        )
        return response['Messages']
