import json
import logging
import os
import time
import uuid

import boto3
from botocore.client import Config

from functions.helpers import create_presigned_url
from functions.helpers import to_dynamo

logger = logging.getLogger()
logger.setLevel(logging.INFO)

## Generates blob id and save blob id, callback url into Dynamo DB table

# Return upload HTML page with info + presigned URL
def create(event, context):

    # Read event body
    data = json.loads(event['body'])
    
    # Creates blob info
    blob_info = to_dynamo(data)
    # Creates URL info
    url_info = create_presigned_url(blob_info)

    body = {
        'blob_id': blob_info['id'],
        'callback_url': blob_info['callback_url'],
        'upload_url': url_info['url']
    }
    
    return {
        "statusCode" : 200,
        "body" : json.dumps(body)
    } 

