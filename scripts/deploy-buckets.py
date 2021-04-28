import argparse
import common
import os

def create_stack(stack_name, glue_bucket_name, raw_data_bucket_name, processed_data_bucket_name, athena_bucket_name, glue_scripts_bucket_name, taskcat_bucket_name):
    stack_parameters = [
            {'ParameterKey': 'S3GlueBucketName', 'ParameterValue': glue_bucket_name},
            {'ParameterKey': 'S3RawDataBucketName', 'ParameterValue': raw_data_bucket_name},
            {'ParameterKey': 'S3ProcessedDataBucketName', 'ParameterValue': processed_data_bucket_name},
            {'ParameterKey': 'S3AthenaBucketName', 'ParameterValue': athena_bucket_name},
            {'ParameterKey': 'S3GlueScriptsBucketName', 'ParameterValue': glue_scripts_bucket_name},
            {'ParameterKey': 'S3TaskcatBucketName', 'ParameterValue': taskcat_bucket_name}
    ]
    dir_path = os.path.dirname(__file__)
    template_path = os.path.join(dir_path, '..', 'aws/cfn/Buckets.yaml')
    common.create_stack(stack_name, stack_parameters, template_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--StackName', required=True, help='Name for the CloudFormation Stack')
    parser.add_argument('--S3GlueBucketName', required=True, help='Name of the S3 Bucket for Open API definitions')
    parser.add_argument('--S3RawDataBucketName', required=True, help='Name of the S3 Bucket for lambda functions')
    parser.add_argument('--S3ProcessedDataBucketName', required=True, help='Name of the S3 Bucket for lambda functions')
    parser.add_argument('--S3AthenaBucketName', required=True, help='Name of the S3 Bucket for lambda functions')
    parser.add_argument('--S3GlueScriptsBucketName', required=True, help='Name of the S3 Bucket for lambda functions')
    parser.add_argument('--S3TaskcatBucketName', required=True, help='Name of the S3 Bucket for lambda functions')
    args = parser.parse_args()
    try:
        if common.stack_exists(args.StackName):
            pass
        else:
            create_stack(args.StackName,
                         args.S3GlueBucketName,
                         args.S3RawDataBucketName,
                         args.S3ProcessedDataBucketName,
                         args.S3AthenaBucketName,
                         args.S3GlueScriptsBucketName,
                         args.S3TaskcatBucketName)
    except Exception as e:
        print(e)
        exit(1)