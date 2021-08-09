# Blob Rekognition

These scripts deploy APIs and Python functions allowing us to POST an image in JPEG and receive the relavant labels after passing it through the AWS Rekognition service. 

AWS services used are API Gateway, Lambda, DynamoDB, S3 and Rekognition.

The serverless.yaml file consists of the AWS infrastructure configuration for deployment via CloudFormation.

The functions folder consists of backend logic in Python.
