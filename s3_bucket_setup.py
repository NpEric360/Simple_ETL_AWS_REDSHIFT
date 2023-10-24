import boto3

access_key = ''
secret_key = ''

s3= boto3.resource("s3", aws_access_key_id = access_key, aws_secret_access_key = secret_key)
#establish connection to s3 using AWS credentials
s3_client = boto3.client("s3", aws_access_key_id = access_key, aws_secret_access_key = secret_key)

#1. Create bucket
def create_bucket():
    try:
        s3_client.create_bucket(Bucket=S3_BUCKET_NAME)
    except Exception as e:
        print(e)

S3_BUCKET_NAME = 'PROJECT2_TEST'
#create_bucket()