import boto3
from botocore.exceptions import ClientError
import time
import logging
import os
import botocore


def vpc_create():
    ec2 = boto3.client('ec2')

    response = ec2.describe_vpcs()
    vpc_id = response.get('Vpcs', [{}])[0].get('VpcId', '')

    # logging
    logger = logging.getLogger('vpcass')
    hdlr = logging.FileHandler('vpcass.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)


    for i in range(10):
        try:
            response = ec2.create_security_group(GroupName='himdurua'+str(i),
                                                 Description='Made by boto3',
                                                 VpcId=vpc_id)
            security_group_id = response['GroupId']
            print('Security Group Created %s in vpc %s.' % (security_group_id, vpc_id))

            data = ec2.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {'IpProtocol': 'tcp',
                     'FromPort': 80,
                     'ToPort': 80,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp',
                     'FromPort': 22,
                     'ToPort': 22,
                     'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ])
            print('Ingress Successfully Set %s' % data)

            logger.info(response['GroupId'])

            timeout = time.time() + 5   # 5 seconds from now
            while True:
                if time.time() > timeout:
                    break


        except ClientError as e:
            print(e)
            logger.error('exception occurred')



def vpc_delete():
# Create EC2 client

    client = boto3.client('ec2')

    result = client.describe_security_groups()

    # logging
    logger = logging.getLogger('vpcass')
    hdlr = logging.FileHandler('vpcass.log')
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    # Delete security group
    try:
        for value in result["SecurityGroups"]:
            if value["GroupName"] == 'default':
                pass
            elif value["GroupName"] == 'launch-wizard-1':
                pass
            else:
                response = client.delete_security_group(GroupId=value["GroupId"])
                logger.info(value['GroupId'])
                print('Security Group Deleted')

    except ClientError as e:
        print(e)
        logger.error('exception occurred')






def upload_logfile():

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


if __name__ == '__main__':
    vpc_create()
    vpc_delete()
    upload_logfile()
