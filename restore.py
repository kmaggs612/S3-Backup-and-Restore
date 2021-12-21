import boto3
import os
import sys
from botocore.client import ClientError

s3 = boto3.client("s3")
resource = boto3.resource("s3")


if len(sys.argv) < 3:
    print("Error: bucket name and/or directory name not specified.")
else:
    bucketName = sys.argv[1]
    rootName = sys.argv[2]

    bucket = resource.Bucket(bucketName)

    try:
        # check if bucket exists and is accessible
        resource.meta.client.head_bucket(Bucket = bucketName)
    except ClientError:
        print("Error: bucket does not exist or you do not have access to it.")
        quit()
    print("Restoring directory...")
    restore = os.path.join(rootName, "Restore")
    # make directory for Restore folder if one does not already exist
    if not os.path.isdir(restore):
        os.mkdir(restore)

    for file in bucket.objects.all():
        dir = os.path.dirname(file.key)
        dir = os.path.join(rootName, "Restore", dir)
        # make directories in path if any do not already exist
        if not os.path.exists(dir):
            os.makedirs(dir)
        s3.download_file(bucketName, file.key, os.path.join(rootName, "Restore", file.key))
    print("All done!")
