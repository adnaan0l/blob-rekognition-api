import json
import logging
import boto3

from functions.helpers import create_presigned_url, to_dynamo

logger = logging.getLogger()
logger.setLevel(logging.INFO)

'''
Create function

To generates and save the blob id, callback url, timestamps into DynamoDB
'''
def create(event, context):

    try:
        data = json.loads(event['body'])
        data['callback_url']
        
        # Creates blob info
        blob_info = to_dynamo(data)

        # Creates URL info
        url_info = create_presigned_url(blob_info)

    except Exception as e:
        logger.error(e)
        return {
            "statusCode" : 401,
            "body" : json.dumps('Error. Please contact admin.')
        }
    else:
        body = {
            'blob_id': blob_info['id'],
            'callback_url': blob_info['callback_url'],
            'upload_url': url_info['url']
        }
        
        return {
            "statusCode" : 200,
            "body" : json.dumps(body)
        } 

