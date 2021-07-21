import logging
import os
import json
import time
import uuid
import boto3
from botocore.client import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

'''
Load environment variables
'''
bucket_name = os.environ['S3_BUCKET']
table_name = os.environ['DYNAMODB_TABLE']

# Initiate clients
dynamodb = boto3.resource('dynamodb')

# Generate timestamp
timestamp = str(time.time())


'''
Insert to DynamoDB
'''
def to_dynamo(data):

    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    item = {
        'id': str(uuid.uuid1()),
        'data': "",
        'callback_url' : data['callback_url'],
        'checked': False,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    response = table.put_item(Item=item)
    
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logger.error('Error. Failed to insert record id: {}'.format(item['id']))
        logger.error(response)
        raise Exception("DB Insert failed exception")
    else:
        logger.info('Successfully inserted record id: {}'.format(item['id']))
        
        return {
            "id" : item["id"],
            "callback_url" : item["callback_url"]
        }

'''
Create a presigned URL
'''
def create_presigned_url(blob_info):
    s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))    
    object_name = "uploads/"+blob_info["id"]+".jpg"
    expiration = 3600
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
        raise Exception("Signed URL creation failed exception")
    else:
        return {
            'url' : url,
            'expiration' : expiration
        }

'''
Detect labels
'''
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

'''
Fetch data from DynamoDB
'''
def fetch_data(blob_id):
    table = dynamodb.Table(table_name)
    # Fetch blob info from the database
    response = table.get_item(
        Key={
            'id': blob_id
        }
    )
    return response


'''
Insert data into DynamoDB
'''
def insert_data(blob_id, labels):
    table = dynamodb.Table(table_name)
    response = table.update_item(
        Key={
            'id': blob_id
        },
        ExpressionAttributeNames={
          '#labels': 'data',
        },
        ExpressionAttributeValues={
          ':data': json.dumps(labels),
          ':checked': True,
          ':updatedAt': timestamp
        },
        UpdateExpression='SET #labels = :data, '
                         'checked = :checked, '
                         'updatedAt = :updatedAt',
        ReturnValues='NONE',
    )
    return response