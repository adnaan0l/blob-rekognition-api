import requests
import logging
import boto3

def return_blob(event, context):
    
    # Get record
    record = event['Records'][0]

    # Get call back URL
    callback_url = record['NewImage']['callback_url']['S']

    blob_id = record['NewImage']['id']['S']

    rekognition_data =  record['NewImage']['data']['S']

    # POST to callback URL
    r = requests.post("{}/{}".format(callback_url, blob_id), data=rekognition_data)

    # Check for errors
    if r.status_code == 200:
        logging.info('Success. Returned Rekognition data')
    else:
        logging.error('Error. Please check args.')
        logging.error(r)
