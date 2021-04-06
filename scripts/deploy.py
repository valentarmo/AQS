import argparse
import boto3
import time
import sys
import os

from botocore.exceptions import ClientError


def deploy_stack(stack_name, region, client):
    if stack_exists(stack_name, client):
        update_stack(stack_name, region, client)
        wait_until_stack_is_updated(stack_name, client)
    else:
        create_stack(stack_name, region, client)
        wait_until_stack_is_created(stack_name, client)


def stack_exists(stack_name, client):
    try:
        client.describe_stacks(StackName=stack_name)
        return True
    except ClientError:
        return False


def update_stack(stack_name, region, client):
    print('Updating CloudFormation Stack')
    dir_path = os.path.dirname(__file__)
    template_path = os.path.join(dir_path, '../', 'cloudformation/', 'DataLake.yaml')
    template_body = ''
    with open(template_path, 'r') as f:
        template_body = f.read()
    response = client.update_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Parameters=[
            {'ParameterKey': 'Region', 'ParameterValue': region}
        ],
        Capabilities=['CAPABILITY_NAMED_IAM']
    )


def wait_until_stack_is_updated(stack_name, client):
    status = client.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    while status not in ['UPDATE_FAILED', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE']:
        time.sleep(5)
        status = client.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    if status == 'UPDATE_CREATE_FAILED' or status == 'UPDATE_ROLLBACK_COMPLETE':
        raise Exception('Stack Update Failed')
    print('Stack Updated')


def create_stack(stack_name, region, client):
    print('Creating CloudFormation Stack')
    dir_path = os.path.dirname(__file__)
    template_path = os.path.join(dir_path, '../', 'cloudformation/', 'DataLake.yaml')
    template_body = ''
    with open(template_path, 'r') as f:
        template_body = f.read()
    response = client.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Parameters=[
            {'ParameterKey': 'Region', 'ParameterValue': region}
        ],
        Capabilities=['CAPABILITY_NAMED_IAM']
    )


def wait_until_stack_is_created(stack_name, client):
    status = client.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    while status not in ['CREATE_FAILED', 'CREATE_COMPLETE', 'ROLLBACK_COMPLETE']:
        time.sleep(5)
        status = client.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    if status == 'CREATE_FAILED' or status == 'ROLLBACK_COMPLETE':
        raise Exception('Stack Creation Failed')
    print('Stack created')


def deploy_scripts(stack_name, client):
    s3 = boto3.client('s3')
    bucket_name = get_scripts_bucket_name(stack_name, client)
    dir_path = os.path.dirname(__file__)
    scripts_home = os.path.join(dir_path, 'ETL')
    for script in os.listdir(scripts_home):
        script_path = os.path.join(scripts_home, script)
        s3.upload_file(script_path, bucket_name, script)


def get_scripts_bucket_name(stack_name, client):
    response = client.describe_stacks(StackName=stack_name)
    return response['Stacks'][0]['Outputs'][0]['OutputValue']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--StackName', required=True, help='Name of the Stack')
    parser.add_argument('--Region', help='Region where to create the Stack', default='us-east-2', choices=['us-west-1', 'us-east-1', 'us-west-2', 'us-east-2'])
    parser.add_argument('--S3BucketPrefix', required=True, help='Prefix for S3 Buckets')
    args = parser.parse_args()

    CloudFormation = boto3.client('cloudformation')
    try:
        deploy_stack(args.StackName, args.KeyName, args.Region, args.PrivateKeyS3Bucket, args.PrivateKeyS3FilePath, CloudFormation)
    except Exception as e:
        print(e)
        sys.exit(1)
