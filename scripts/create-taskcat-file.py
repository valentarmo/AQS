import argparse
import common
import yaml
import sys
import os

def create_taskcat_file(s3_glue_bucket_name, s3_raw_data_bucket_name, s3_processed_data_bucket_name, s3_athena_bucket_name, s3_glue_scripts_bucket_name, s3_taskcat_bucket_name, s3_raw_data_bucket_arn, region):
    dir_path = os.path.dirname(__file__)
    taskcat_file_path = os.path.join(dir_path, '../', '.taskcat.yml')
    contents = {
        'general': {
            'parameters': {
                'S3GlueBucketName': s3_glue_bucket_name,
                'S3RawDataBucketName': s3_raw_data_bucket_name,
                'S3ProcessedDataBucketName': s3_processed_data_bucket_name,
                'S3AthenaBucketName': s3_athena_bucket_name,
                'S3GlueScriptsBucketName': s3_glue_scripts_bucket_name,
                'S3RawDataBucketArn':s3_raw_data_bucket_arn 
            },
            's3_bucket': s3_taskcat_bucket_name
        },
        'project': {
            'name': 'aqs',
            'regions': [region],
        },
        'tests': {
            'creation-test': {
                'template': 'aws/cfn/DataLake.yaml'
            }
        }
    }
    with open(taskcat_file_path, 'w') as f:
        yaml.dump(contents, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--Region', help='Region where to test the Stack', default='us-east-2', choices=['us-west-1', 'us-east-1', 'us-west-2', 'us-east-2'])
    parser.add_argument('--S3GlueBucketName', required=True, help='Bucket name for Glue')
    parser.add_argument('--S3RawDataBucketName', required=True, help='Bucket name for Raw Data')
    parser.add_argument('--S3ProcessedDataBucketName', required=True, help='Bucket name for processed data')
    parser.add_argument('--S3AthenaBucketName', required=True, help='Bucket name for athena')
    parser.add_argument('--S3GlueScriptsBucketName', required=True, help='Bucket name for glue scripts')
    parser.add_argument('--S3TaskcatBucketName', required=True, help='Bucket name for Taskcat')
    args = parser.parse_args()

    try:
        s3_raw_data_bucket_arn = common.get_ssm_parameter_value('AQSS3RawDataBucketArn')
        create_taskcat_file(args.S3GlueBucketName,
                            args.S3RawDataBucketName,
                            args.S3ProcessedDataBucketName,
                            args.S3AthenaBucketName,
                            args.S3GlueScriptsBucketName,
                            args.S3TaskcatBucketName,
                            s3_raw_data_bucket_arn,
                            args.Region)
    except Exception as e:
        print(e)
        sys.exit(1)