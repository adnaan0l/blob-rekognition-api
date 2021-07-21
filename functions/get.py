import os
import json
import logging
import boto3

from functions.helpers import fetch_data

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')

'''
Fetch function

To retrieve blob information from Dynamo DB 
'''
def get(event, context):
    blob_id = event['pathParameters']['blob_id']
    
    # Fetch data
    response = fetch_data(blob_id)

    # Check response valids
    check_response(response, blob_id)

    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logger.error('Error retrieving id: {} failed'.format(blob_id))
        logger.error(response)
        return {
            "statusCode": 401,
            "body": json.dumps('Error')
        }
    else:
        logger.info('Successfully retrieved id: {}'.format(blob_id))
        return {
            "statusCode": 200,
            "body": json.dumps('Success')
        }

    