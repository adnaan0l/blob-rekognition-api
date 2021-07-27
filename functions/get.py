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
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logger.error('Error retrieving id: {} failed'.format(blob_id))
        logger.error(response)
        return {
            "statusCode": 404,
            "body": json.dumps('Blob ID not found')
        }
    else:
        logger.info('Successfully retrieved id: {}'.format(blob_id))
        
        try:
            labels = json.loads(response['Item']['data'])
        except:
            json_data = {
                'blob_id': response['Item']['id'],
                'msg': 'Still processing'
            }
        else:
            json_data = {
                'blob_id': response['Item']['id'],
                'labels': labels['Labels']
            }
        return {
            "statusCode": 200,
            "body": json.dumps(json_data)
        }

    