import argparse
import common
import boto3
import time
import sys
import os

from botocore.exceptions import ClientError


def deploy_stack(stack_name, s3_glue_bucket_name, s3_raw_data_bucket_name, s3_processed_data_bucket_name, s3_athena_bucket_name, s3_glue_scripts_bucket_name, s3_raw_data_bucket_arn):
    parameters = [
        {'ParameterKey': 'S3GlueBucketName', 'ParameterValue': s3_glue_bucket_name},
        {'ParameterKey': 'S3RawDataBucketName', 'ParameterValue': s3_raw_data_bucket_name},
        {'ParameterKey': 'S3ProcessedDataBucketName', 'ParameterValue': s3_processed_data_bucket_name},
        {'ParameterKey': 'S3AthenaBucketName', 'ParameterValue': s3_athena_bucket_name},
        {'ParameterKey': 'S3GlueScriptsBucketName', 'ParameterValue': s3_glue_scripts_bucket_name},
        {'ParameterKey': 'S3RawDataBucketArn', 'ParameterValue': s3_raw_data_bucket_arn}
    ]
    dir_path = os.path.dirname(__file__)
    template_path = os.path.join(dir_path, '../', 'aws/cfn/', 'DataLake.yaml')
    common.deploy_stack(stack_name, parameters, template_path)


def deploy_scripts():
    print('Deploying ETL scripts')
    s3 = boto3.client('s3')
    bucket_name = common.get_ssm_parameter_value('AQSS3GlueScriptsBucketName')
    dir_path = os.path.dirname(__file__)
    scripts_home = os.path.join(dir_path, 'ETL')
    for script in os.listdir(scripts_home):
        script_path = os.path.join(scripts_home, script)
        s3.upload_file(script_path, bucket_name, script)
    print('Scripts deployed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--StackName', required=True, help='Name of the Stack')
    parser.add_argument('--S3GlueBucketName', required=True, help='Bucket name for Glue')
    parser.add_argument('--S3RawDataBucketName', required=True, help='Bucket name for Raw Data')
    parser.add_argument('--S3ProcessedDataBucketName', required=True, help='Bucket name for processed data')
    parser.add_argument('--S3AthenaBucketName', required=True, help='Bucket name for athena')
    parser.add_argument('--S3GlueScriptsBucketName', required=True, help='Bucket name for glue scripts')
    args = parser.parse_args()

    try:
        s3_raw_data_bucket_arn = common.get_ssm_parameter_value('AQSS3RawDataBucketArn')
        deploy_stack(args.StackName,
                     args.S3GlueBucketName,
                     args.S3RawDataBucketName,
                     args.S3ProcessedDataBucketName,
                     args.S3AthenaBucketName,
                     args.S3GlueScriptsBucketName,
                     s3_raw_data_bucket_arn)
        deploy_scripts()
    except Exception as e:
        print(e)
        sys.exit(1)
