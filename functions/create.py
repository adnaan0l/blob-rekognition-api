import json
import logging
import os
import time
import uuid

import boto3

## Generates blob id and save blob id, callback url into Dynamo DB table
def info_to_dynamo(data):

    dynamodb = boto3.resource('dynamodb')
    
    # Validate if callback url is present
    if 'callback_url' not in data:
        logging.error("Validation Failed. No callback URL.")
        raise Exception("ERROR: No callback URL. Cannot initiate task")
    
    # Get current time
    timestamp = str(time.time())

    # Load DynamoDB table
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # Create record for inserting
    item = {
        'id': str(uuid.uuid1()),
        'data': "",
        'callback_url' : data['callback_url'],
        'checked': False,
        'createdAt': timestamp,
        'updatedAt': timestamp,
    }

    # Write record into the database
    response = table.put_item(Item=item)
    
    if response['ResponseMetadata']['HTTPStatusCode'] != 200:
        logging.error("Insert Failed")
        logging.error(response)
    else:
        return {
            "id" : item["id"],
            "callback_url" : item["callback_url"]
        }

## Generates and returns presigned URL 
def create_presigned_url(blob_info):
    s3_client = boto3.client('s3')
    # Load initial parameters
    bucket_name = os.environ['S3_BUCKET']
    object_name = "uploads/"+blob_info["id"]+".png"
    expiration = 300
    # Generate a presigned S3 URL for upload
    try:
        url = s3_client.generate_presigned_url('put_object', 
                                                    Params = {'Bucket': bucket_name,
                                                     'Key': object_name},
                                                     ExpiresIn=expiration)
    except Exception as e:
        logging.error('Error. URL generation failed')
        logging.error(e)
    else:
        return {
            'url' : url,
            'expiration' : expiration
        }

# Return upload HTML page with info + presigned URL
def create(event, context):

    # Read event body
    data = json.loads(event['body'])
    
    # Creates blob info
    blob_info = info_to_dynamo(data)
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

