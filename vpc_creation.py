import boto3
from botocore.exceptions import ClientError
import time
import logging


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
