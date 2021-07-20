import requests
import boto3

def return(event, context):
    
    # Get record
    record = event['Records'][0]

    # Get call back URL
    callback_url = record['NewImage']['callback_url']['S']

    # Create response
    response = {
        'blob_id': record['NewImage']['id']['S'],
        'rekognition_data': record['NewImage']['data']['S']
    }
    
    # POST to callback URL
    r = requests.post(callback_url, data=response)

    # Check for errors
    if r.status_code == 200:
        logging.info('Success. Returned Rekognition data')
    else:
        logging.error('Error Encountered. Please check args.')
        logging.error(r)
