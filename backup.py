import boto3
import os
import sys
from botocore.client import ClientError

s3 = boto3.resource("s3")
client = boto3.client("s3")

if len(sys.argv) < 3:
    print("Error: directory name and/or bucket name not specified.")
else:
    rootName = sys.argv[1]
    bucketName = sys.argv[2]
    try:
        # check if bucket exists and is accessible
        s3.meta.client.head_bucket(Bucket = bucketName)
    except ClientError:
        print("Error: bucket does not exist or you do not have access to it.")
        quit()
    print("Backing up directory...")
    bucket = s3.Bucket(bucketName)
    for dirPath, dirs, files in os.walk(rootName):
        for file in files:
            filePath = os.path.join(dirPath, file)
            name = filePath[len(rootName) + 1:]
            existing = list(bucket.objects.filter(Prefix=name))
            if (len(existing) <= 0 or 
                existing[0].last_modified.timestamp() < os.path.getmtime(filePath)):
                # upload file if not already uploaded or modified since last upload
                s3.meta.client.upload_file(filePath, bucketName, name)
    print("All done!")