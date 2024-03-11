import boto3
from datetime import datetime
#from flask import current_app

def download_csv_from_s3(bucket_name, object_key, download_path):
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, object_key, download_path)
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Return the time of download
