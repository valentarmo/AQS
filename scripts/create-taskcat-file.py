import argparse
import yaml
import sys
import os

def create_taskcat_file(bucket_prefix, region):
    dir_path = os.path.dirname(__file__)
    taskcat_file_path = os.path.join(dir_path, '../', '.taskcat.yml')
    contents = {
        'general': {
            'parameters': {
                'S3BucketPrefix': bucket_prefix
            }
        },
        'project': {
            'name': 'aqs',
            'regions': [region],
        },
        'tests': {
            'creation-test': {
                'template': 'cloudformation/DataLake.yaml'
            }
        }
    }
    with open(taskcat_file_path, 'w') as f:
        yaml.dump(contents, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--S3BucketPrefix', required=True, help='Prefix for S3 Buckets')
    parser.add_argument('--Region', help='Region where to test the Stack', default='us-east-2', choices=['us-west-1', 'us-east-1', 'us-west-2', 'us-east-2'])
    args = parser.parse_args()

    try:
        create_taskcat_file(args.S3BucketPrefix, args.Region)
    except Exception as e:
        print(e)
        sys.exit(1)