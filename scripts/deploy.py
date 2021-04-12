import argparse
import boto3
import time
import sys
import os

from botocore.exceptions import ClientError


def deploy_stack(stack_name, s3_bucket_prefix, cloudformation):
    if stack_exists(stack_name, cloudformation):
        update_stack(stack_name, s3_bucket_prefix, cloudformation)
        wait_until_stack_is_updated(stack_name, cloudformation)
    else:
        create_stack(stack_name, s3_bucket_prefix, cloudformation)
        wait_until_stack_is_created(stack_name, cloudformation)


def stack_exists(stack_name, cloudformation):
    try:
        cloudformation.describe_stacks(StackName=stack_name)
        return True
    except ClientError:
        return False


def update_stack(stack_name, s3_bucket_prefix, cloudformation):
    print('Updating CloudFormation Stack')
    template_body = get_cloudformation_template()
    response = cloudformation.update_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Parameters=[
            {'ParameterKey': 'S3BucketPrefix', 'ParameterValue': s3_bucket_prefix}
        ],
        Capabilities=['CAPABILITY_NAMED_IAM']
    )


def wait_until_stack_is_updated(stack_name, cloudformation):
    status = cloudformation.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    while status not in ['UPDATE_FAILED', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE']:
        time.sleep(5)
        status = cloudformation.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    if status == 'UPDATE_CREATE_FAILED' or status == 'UPDATE_ROLLBACK_COMPLETE':
        raise Exception('Stack Update Failed')
    print('Stack Updated')


def create_stack(stack_name, s3_bucket_prefix, cloudformation):
    print('Creating CloudFormation Stack')
    template_body = get_cloudformation_template()
    response = cloudformation.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Parameters=[
            {'ParameterKey': 'S3BucketPrefix', 'ParameterValue': s3_bucket_prefix}
        ],
        Capabilities=['CAPABILITY_NAMED_IAM']
    )


def wait_until_stack_is_created(stack_name, cloudformation):
    status = cloudformation.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    while status not in ['CREATE_FAILED', 'CREATE_COMPLETE', 'ROLLBACK_COMPLETE']:
        time.sleep(5)
        status = cloudformation.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    if status == 'CREATE_FAILED' or status == 'ROLLBACK_COMPLETE':
        raise Exception('Stack Creation Failed')
    print('Stack created')


def get_cloudformation_template():
    dir_path = os.path.dirname(__file__)
    template_path = os.path.join(dir_path, '../', 'cloudformation/', 'DataLake.yaml')
    template_body = ''
    with open(template_path, 'r') as f:
        template_body = f.read()   
    return template_body


def deploy_scripts(stack_name, cloudformation):
    print('Deploying ETL scripts')
    s3 = boto3.client('s3')
    bucket_name = get_scripts_bucket_name(stack_name, cloudformation)
    dir_path = os.path.dirname(__file__)
    scripts_home = os.path.join(dir_path, 'ETL')
    for script in os.listdir(scripts_home):
        script_path = os.path.join(scripts_home, script)
        s3.upload_file(script_path, bucket_name, script)
    print('Scripts deployed')


def get_scripts_bucket_name(stack_name, cloudformation):
    print('Getting Scripts Bucket Name')
    response = cloudformation.describe_stacks(StackName=stack_name)
    return response['Stacks'][0]['Outputs'][0]['OutputValue']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--StackName', required=True, help='Name of the Stack')
    parser.add_argument('--S3BucketPrefix', required=True, help='Prefix for S3 Buckets')
    args = parser.parse_args()

    CloudFormation = boto3.client('cloudformation')
    try:
        deploy_stack(args.StackName, args.S3BucketPrefix,  CloudFormation)
        deploy_scripts(args.StackName, CloudFormation)
    except Exception as e:
        print(e)
        sys.exit(1)
