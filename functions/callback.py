import json
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

'''
Callback function

To test the POST to the callback URL
'''
def callback(event, context):

    logger.info("Success. Callback received.")
    print(event)
    
    return {
        "statusCode" : 200,
        "body" : json.dumps('success')
    } 
