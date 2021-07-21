import os
import json
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')


def get(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    blob_id = event['pathParameters']['blob_id']
    
    # Fetch blob info from the database
    response = table.get_item(
        Key={
            'id': blob_id
        }
    )
    
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logger.error('Error. Fetch failed record id: {}'.format(blob_id))
        logger.error(response)
    else:
        logger.info('Successfully fetched record id: {}'.format(blob_id))

    return {
        "statusCode": 200,
        "body": json.dumps(response['Item'])
    }