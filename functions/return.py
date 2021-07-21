import requests
import logging
import boto3

from functions.helpers import update_posted

logger = logging.getLogger()
logger.setLevel(logging.INFO)

'''
Return function

To POST generated label data to the user's callback URL
'''
def return_blob(event, context):

    # Get record
    record = event['Records'][0]['dynamodb']['NewImage']

    # Get callback URL
    callback_url = record['callback_url']['S']

    blob_id = record['id']['S']

    rekognition_data =  record['data']['S']

    logger.info("Posting rekognition data to {}/{}".format(callback_url, blob_id))

    # POST to callback URL
    r = requests.post("{}/{}".format(callback_url, blob_id), data=rekognition_data)

    # Check for errors
    if r.status_code == 200:
        logging.info('Successfully posted Rekognition data to {}/{} for id: {}'.format(callback_url, blob_id, blob_id))
    
    else:
        logging.error('Failed posting data to {}/{} for id: {}. Please check args.'.format(callback_url, blob_id, blob_id))
        logging.error(r)
