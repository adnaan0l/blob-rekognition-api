import json
import logging
import os
import time
import uuid

import boto3
from botocore.client import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

## Generates blob id and save blob id, callback url into Dynamo DB table

# Return upload HTML page with info + presigned URL
def callback(event, context):

    print(event)
    
    return {
        "statusCode" : 200,
        "body" : json.dumps('success')
    } 
