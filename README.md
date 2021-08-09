# Blob Rekognition

These scripts deploy APIs and Python functions allowing us to POST an image in JPEG and receive information about its contents as labels after passing it through the AWS Rekognition service. 

AWS services used are API Gateway, Lambda, DynamoDB, S3 and Rekognition.

The serverless.yml file consists of the AWS infrastructure configuration for deployment via CloudFormation.

The openapi.yml file consists fo the structure of the API according to the Open API Specification.

The functions folder consists of backend logic in Python.

The following API paths are created,

  - /blobs : The path to POST the blob. A callback URL must be provided when making a POST.
  - /blobs/{blob_id} - The path to retrieve information about a particular blob id.
