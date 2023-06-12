import random
import boto3
import os
import io
import base64

s3_client = boto3.client('s3')

def random_image(bucket_name):
    response = s3_client.list_objects_v2(Bucket=bucket_name)
    # print(response)
    
    if 'Contents' in response:
        objects = response['Contents']
        # print(objects)
        random_object = random.choice(objects)
        print('random_object',random_object)
        object_key = random_object['Key']
        print('object_key', object_key)
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        
        image_data = response['Body'].read()

        # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-download-file.html

        return image_data


# Base64 trick
# https://docs.aws.amazon.com/apigateway/latest/developerguide/lambda-proxy-binary-media.html
def lambda_handler(event, context):
    bucket_name = os.environ.get('S3_BUCKET')
    if bucket_name:
        image_data = random_image(bucket_name)
        if image_data:
            return {
                'isBase64Encoded': True,
                'statusCode': 200,
                'body': base64.b64encode(image_data).decode('utf-8'),
                'headers': {
                    'Content-Type': 'image/jpeg'
                }
            }

    return {
        'statusCode': 400,
        'body': 'Invalid request'
    }
