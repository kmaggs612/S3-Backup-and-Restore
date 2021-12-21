# S3-Backup-and-Restore

Backup:
Backup must be run with arguments for the absolute path of the directory to be backed up and the name of the S3 bucket to back the files up to. If either of these arguments is not given, if they are given in the wrong order, or if the bucket given is not one that already exists and is accessible by the account in the .aws configuration file, the program prints an error statement.
	If the arguments are given correctly, the program recursively traverses the directory with os.walk, uploading all files to S3 with boto3.resource.meta.client.upload_file and preserving their paths. If a file already exists in S3 and has not been modified since it was last backed up, the program avoids moving data needlessly by comparing the modification times.

Restore:
Restore must be run with arguments for the name of the S3 bucket to restore files from and the absolute path of the directory to download the restoration into. If either of these arguments is not given, if they are given in the wrong order, or if the bucket given is not one that already exists and is accessible by the account in the .aws configuration file, the program prints an error statement.
	If the arguments are given correctly, the program downloads all the files with boto3.client.download_file into a directory called Restore so they can easily be distinguished from other files that might share the same name. The original structure of the files is preserved within the new directory.
