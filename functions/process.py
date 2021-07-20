import json
import time
import logging
import os

import boto3
dynamodb = boto3.resource('dynamodb')


def update(event, context):

    # Dummy return from Rekognition service
    recognition_data = {
        'label_one': "string_one",
        'label_two': "string_two",
    }
    #-------------------

    # Get current time
    timestamp = int(time.time() * 1000)

    # Load DynamoDB table
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # Update the record in the database
    response = table.update_item(
        Key={
            'id': event['pathParameters']['id']
        },
        ExpressionAttributeNames={
          '#recongition_data': 'text',
        },
        ExpressionAttributeValues={
          ':text': json.dumps(recognition_data),
          ':updatedAt': timestamp,
        },
        UpdateExpression='SET #recongition_data = :text, '
                         'checked = :checked, '
                         'updatedAt = :updatedAt',
        ReturnValues='NONE',
    )

    # Check if update success
    try:
        response['Attributes']
    except:
        logging.error('Error. Update failed.')
        logging.error(response)
    else:

        logging.info('Success. Record updated.')

