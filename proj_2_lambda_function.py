import json
import urllib.parse
import boto3
import psycopg2

s3 = boto3.client('s3')

def lambda_handler(event,context):

     # Retrieve the bucket name and object key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    # Retrieve the file contents from S3
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    #file_contents = response['Body'].read().decode('utf-8')
    
    text = response["Body"].read().decode()
    data = json.loads(text)
    print(data)
    print("CONTENT TYPE: " + response['ContentType'])

    #redshift connection
    try:
        conn = psycopg2.connect(dbname = 'dev',
                                host = 'redshift-cluster-1.cdssr3vsbqjq.us-east-1.redshift.amazonaws.com',
                                port = '5439',
                                user = 'nperic360@gmail.com',
                                password = 'DefaultPass1')
        
        cursor = conn.cursor()
        
        #Parse response body
        # Accessing the "profiles" dictionary
        profiles = data["profiles"]
        
        # Iterate over each user and store in the table if the state is "CA"
        for person_name, person_data in profiles.items():
            if person_data["state"] == "CA":
                # Extract user information
                name = person_name
                address = person_data["address1"]
                occupation = person_data["Occupation"]
                try:
                    # Insert user information into the SQL table
                    insert_query = "INSERT INTO table1 (name, address, occupation) VALUES (%s, %s, %s)"
                    values = (name, address, occupation)
                    cursor.execute(insert_query, values)
                except Exception as e:
                    print("error A : ", e)
            
        # Commit the changes and close the cursor and connection
        conn.commit()
        cursor.close()
        conn.close()
        
    except Exception as e:
        print("error B :", e)
        
    
    return {
             # Convert event to JSON string
        'event_json' : json.dumps(event),
        'statusCode':200,
        'body':json.dumps("Hello World")
    }