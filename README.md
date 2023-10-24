# Simple_ETL_AWS_REDSHIFT
This pipeline calls a Flask API GET method to generate data which is uploaded to an AWS S3 bucket. This triggers a Lambda function that warehouses this data in Amazon Redshift.

Order of execution:

1. Start Flask API: fake_profile_flask.py
2. Setup AWS S3 Bucket for first-time use: s3_bucket_setup.py
3. Perform an API call and upload the generated .json files to S3 Bucket: main_api_s3_upload.py

Setup AWS Lambda function:
1. Create a Redshift Cluster, edit proj_2_lambda_function.py 'conn = psycopg2.connect' credentials
2. Set the S3 bucket as the trigger and copy proj_2_lambda_function
3. Make sure the correct IAM permissions are set for each step if necessary.
