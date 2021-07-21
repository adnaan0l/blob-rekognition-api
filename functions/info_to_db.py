import json
import logging
import os
import time
import uuid

import boto3
from botocore.client import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def to_dynamo(data):

    dynamodb = boto3.resource('dynamodb')
    
    # Validate if callback url is present
    if 'callback_url' not in data:
        logging.error("Validation Failed. No callback URL.")
        raise Exception("ERROR: No callback URL. Cannot initiate task")
    
    # Get current time
    timestamp = str(time.time())

    # Load DynamoDB table
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # Create record for inserting
    item = {
        'id': str(uuid.uuid1()),
        'data': "",
        'callback_url' : data['callback_url'],
        'checked': False,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    # Write record into the database
    response = table.put_item(Item=item)
    
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logger.error('Error. Failed to insert record id: {}'.format(item['id']))
        logger.error(response)
    else:
        logger.info('Successfully inserted record id: {}'.format(item['id']))
        
        return {
            "id" : item["id"],
            "callback_url" : item["callback_url"]
        }