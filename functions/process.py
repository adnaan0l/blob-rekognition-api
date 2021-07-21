import logging
import json
import boto3

from functions.helpers import detect_labels, insert_data

logger = logging.getLogger()
logger.setLevel(logging.INFO)

'''
Process function

To detect labels and insert into Dynamo DB 
'''
def process(event, context):

    blob_object = event['Records'][0]['s3']['object']['key']
    
    # Get labels
    labels = detect_labels(blob_object)

    # Get blob ID
    blob_id = blob_object.split('/')[1].split('.')[0]

    # Perform data insert
    response = insert_data(blob_id, labels)

    # Check valid response
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logger.error('Error processing id: {} failed.'.format(blob_id))
        logger.error(response)
        return {
            "statusCode": 401,
            "body": json.dumps('Error')
        }
    else:
        logger.info('Successfully processed id: {} updated.'.format(blob_id))
        return {
            "statusCode": 200,
            "body": json.dumps('Success')
        }
