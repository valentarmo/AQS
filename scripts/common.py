import boto3
import time
import sys
import os

from botocore.exceptions import ClientError


__CLOUDFORMATION = boto3.client('cloudformation')


def get_ssm_parameter_value(parameter_name):
    print(f'Getting {parameter_name} from SSM')
    ssm = boto3.client('ssm')
    parameter_value = ssm.get_parameter(Name=parameter_name)['Parameter']['Value']
    return parameter_value


def deploy_stack(stack_name, stack_parameters, template_path):
    if stack_exists(stack_name):
        update_stack(stack_name, stack_parameters, template_path)
    else:
        create_stack(stack_name, stack_parameters, template_path)


def stack_exists(stack_name):
    try:
        __CLOUDFORMATION.describe_stacks(StackName=stack_name)
        return True
    except ClientError:
        return False


def create_stack(stack_name, stack_parameters, template_path):
    print(f'Creating Stack: {stack_name}')
    template_body = ''
    with open(template_path, 'r') as f:
        template_body = f.read()
    __CLOUDFORMATION.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Parameters=stack_parameters,
        Capabilities=['CAPABILITY_NAMED_IAM']
    )
    _wait_until_stack_is_created(stack_name)
    print('Stack Created')


def _wait_until_stack_is_created(stack_name):
    status = __CLOUDFORMATION.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    while status not in ['CREATE_FAILED', 'CREATE_COMPLETE', 'ROLLBACK_COMPLETE']:
        time.sleep(5)
        status = __CLOUDFORMATION.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    if status == 'CREATE_FAILED' or status == 'ROLLBACK_COMPLETE':
        raise Exception('Stack Creation Failed')


def update_stack(stack_name, stack_parameters, template_path):
    print(f'Updating Stack: {stack_name}')
    template_body = ''
    with open(template_path, 'r') as f:
        template_body = f.read()
    response = __CLOUDFORMATION.update_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Parameters=stack_parameters,
        Capabilities=['CAPABILITY_NAMED_IAM']
    )
    _wait_until_stack_is_updated(stack_name)
    print('Stack Updated')


def _wait_until_stack_is_updated(stack_name):
    status = __CLOUDFORMATION.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    while status not in ['UPDATE_FAILED', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE']:
        time.sleep(5)
        status = __CLOUDFORMATION.describe_stacks(StackName=stack_name)['Stacks'][0]['StackStatus']
    if status == 'UPDATE_CREATE_FAILED' or status == 'UPDATE_ROLLBACK_COMPLETE':
        raise Exception('Stack Update Failed')
    print('Stack Updated')