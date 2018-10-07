import boto3
import os
import botocore



s3 = boto3.client('s3', region_name="ap-southeast-1")
s3_up = boto3.resource('s3')
files = os.listdir("./")

# Call S3 to list current buckets
response = s3.list_buckets()

# Get a list of all bucket names from the response
buckets = [bucket['Name'] for bucket in response['Buckets']]

bucket_name = 'sungjun-bucket'
key = 'vpcass.log'

# # Print out the bucket list
# print("Bucket List: %s" % buckets)

# create bucket
if 'sungjun-bucket' in buckets:
    pass

else:
    response = s3.create_bucket(
        Bucket='sungjun-bucket',
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-southeast-1'
            }
        )

# upload files
if 'sungjun-bucket' in buckets:
    try:
        s3_up.Bucket(bucket_name).download_file(key, 're.vpcass.log')
        print("vpcass.log file download as re.vpcass.log!!")


        f = open('C:\\workspace\\big_data\\submit\\vpcass.log', 'r')
        lines = f.readlines()
        f_1 = open('C:\\workspace\\big_data\\submit\\re.vpcass.log', 'r')
        lines_1 = f_1.readlines()
        w = open('C:\\workspace\\big_data\\submit\\re.vpcass.log', 'a')

        for i in range(len(lines)):
            if lines[i] in lines_1:
                pass
            else:
                w.write(lines[i])
        f.close()
        f_1.close()
        w.close()

        for filename in files:
            if filename == 're.vpcass.log':
                s3.upload_file(filename, bucket_name, 'vpcass.log')
                print("vpcass.log file upload!!")


    except botocore.exceptions.ClientError as e:

        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise

        for filename in files:
            if filename == 'vpcass.log':
                s3.upload_file(filename, bucket_name, filename)
                print("vpcass.log file upload!!")
