import boto3
from botocore.exceptions import ClientError
import logging

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
