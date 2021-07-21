import json
import logging
import os
import time
import uuid

import boto3
from botocore.client import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

bucket_name = os.environ['S3_BUCKET']

# Insert data to Dynamo DB
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

## Generates and returns presigned URL 
def create_presigned_url(blob_info):
    s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))
    # Load initial parameters
    
    object_name = "uploads/"+blob_info["id"]+".jpg"
    expiration = 3600
    # Generate a presigned S3 URL for upload
    try:
        url = s3_client.generate_presigned_url('put_object', 
                                                Params={    'Bucket': bucket_name,
                                                            'Key': object_name
                                                            },
                                                ExpiresIn=expiration,
                                                HttpMethod="PUT")
                                                
    except Exception as e:
        logging.error('Error. URL generation failed')
        logging.error(e)
    else:
        return {
            'url' : url,
            'expiration' : expiration
        }

def detect_labels(object):

    rekognition = boto3.client('rekognition')


    response = rekognition.detect_labels(
    Image={
        'S3Object': {
            'Bucket': bucket_name,
            'Name': object
        }
    },
    MaxLabels=3
    )
    return response