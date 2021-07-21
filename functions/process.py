import json
import time
import logging
import os
import boto3

from functions.helpers import detect_labels

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')

def process(event, context):

    object = event['Records'][0]['s3']['object']['key']
    labels = detect_labels(object)

    # Get current time
    timestamp = int(time.time() * 1000)

    # Load DynamoDB table
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    
    blob_id = object.split('/')[1].split('.')[0]
    
    # Update the record in the database
    response = table.update_item(
        Key={
            'id': blob_id
        },
        ExpressionAttributeNames={
          '#labels': 'text',
        },
        ExpressionAttributeValues={
          ':text': json.dumps(labels),
          ':checked': True,
          ':updatedAt': timestamp
        },
        UpdateExpression='SET #labels = :text, '
                         'checked = :checked, '
                         'updatedAt = :updatedAt',
        ReturnValues='NONE',
    )

    # Check if update success
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logger.error('Error.Record id: {} failed.'.format(blob_id))
        logger.error(response)
    else:
        logger.info('Success. Record id: {} updated.'.format(blob_id))

