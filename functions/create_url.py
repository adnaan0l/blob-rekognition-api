import json
import logging
import os
import time
import uuid

import boto3
from botocore.client import Config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

## Generates and returns presigned URL 
def create_presigned_url(blob_info):
    s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))
    # Load initial parameters
    bucket_name = os.environ['S3_BUCKET']
    object_name = "uploads/"+blob_info["id"]+".jpg"
    expiration = 3600
    # Generate a presigned S3 URL for upload
    try:
        url = s3_client.generate_presigned_url('put_object', 
                                                Params={    'Bucket': bucket_name,
                                                            'Key': object_name
                                                            },
                                                ExpiresIn=expiration,
                                                HttpMethod="PUT")
                                                
    except Exception as e:
        logging.error('Error. URL generation failed')
        logging.error(e)
    else:
        return {
            'url' : url,
            'expiration' : expiration
        }