
"""
This ETL Pipeline flows as:
1. HTTP API Get request for json data
2. Store json data to temp directory
3. Upload temp files to AWS S3
4. Create Lambda function that is triggered by AWS S3 put
5. Lambda functions performs filtering and loading:
A) Filter duplicates
B) Store processed data into a data warehouse

"""
import requests
import tempfile
import json
import os
import boto3
from datetime import datetime

BATCH_SIZE = 1
S3_BUCKET_NAME = 'PROJECT2_TEST'
#Start fake_profile_flask.py Flask web application.

def call_profile_api(number_of_profiles):
    response = requests.get(f'http://127.0.0.1:5000/api/profiles?count={number_of_profiles}')
    if response.status_code == 200:
        response_json = response.json()
        return response_json
    else:
        print(f"Error: {response.status} - {response.reason}")

#Write current batch of profiles to a .json file in a temporary directory

def write_to_temp_dir(data,batch_ID,temp_dir):
    temp_file_path = os.path.join(temp_dir,str(batch_ID)+'.json')
    with open(temp_file_path, 'w') as file:
        json.dump(data,file) 

# Call API GET method and write to temporary directory by batches
def download_data(N): 
    temp_dir = tempfile.mkdtemp() #create a temporary subdirectory to save all temporary files to
    for i in range(0,N,BATCH_SIZE):
        batch = call_profile_api(BATCH_SIZE)
        write_to_temp_dir(batch,i,temp_dir) #write current batch to temporary subdirectory
    return temp_dir #return the main temp subdirectory for future calling

###AWS S3 Bucket setup

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


#2. Upload Data to S3 bucket
def get_current_utc_time():
    current_time = datetime.utcnow()
    utc_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S UTC")
    return utc_time_str

def upload_to_s3(temp_directory, bucket_name):
    KEY = get_current_utc_time()
    i=0
    for data in os.listdir(temp_directory):
        s3_client.upload_file(temp_directory+"/"+data, S3_BUCKET_NAME, KEY + data)
        i+=1
    print("number of items uploaded = ",i)

#3. View S3 Bucket contents
def view_contents_in_s3_bucket():
    bucket = s3.Bucket(S3_BUCKET_NAME)
    for obj in bucket.objects.all():
        key = obj.key
        body = obj.get()['Body'].read()
        print(key,body)
    print(key)
    print(json.loads(body))



def main():
    temp_directory = download_data(100)
    print(os.listdir(temp_directory))
    upload_to_s3(temp_directory)
    
#create_bucket()
main()