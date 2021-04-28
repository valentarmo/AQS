pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
    }
    stages {
        stage('Deploy Buckets') {
            steps {
                withEnv(['PATH+EXTRA=/usr/local/bin']) {
                    echo 'Starging bucket deployment'
                    sh "python3 scripts/deploy-buckets.py --StackName ${env.AQS_BUCKETS_STACK_NAME} --S3GlueBucketName ${env.AQS_S3_GLUE_BUCKET_NAME} --S3RawDataBucketName ${env.AQS_S3_RAW_DATA_BUCKET_NAME} --S3ProcessedDataBucketName ${env.AQS_S3_PROCESSED_DATA_BUCKET_NAME} --S3AthenaBucketName ${env.AQS_S3_ATHENA_BUCKET_NAME} --S3GlueScriptsBucketName ${env.AQS_S3_GLUE_SCRIPTS_BUCKET_NAME} --S3TaskcatBucketName ${env.AQS_S3_TASKCAT_BUCKET_NAME}"
                    echo 'Finished bucket deployment'
                }
            }
        }
        stage('Test Stack') {
            steps {
                withEnv(['PATH+EXTRA=/usr/local/bin']) {
                    echo 'Starting Infrastructure Tests'
                    sh "python3 scripts/create-taskcat-file.py --Region ${env.AWS_DEFAULT_REGION} --S3GlueBucketName ${env.AQS_S3_GLUE_BUCKET_NAME} --S3RawDataBucketName ${env.AQS_S3_RAW_DATA_BUCKET_NAME} --S3ProcessedDataBucketName ${env.AQS_S3_PROCESSED_DATA_BUCKET_NAME} --S3AthenaBucketName ${env.AQS_S3_ATHENA_BUCKET_NAME} --S3GlueScriptsBucketName ${env.AQS_S3_GLUE_SCRIPTS_BUCKET_NAME} --S3TaskcatBucketName ${env.AQS_S3_TASKCAT_BUCKET_NAME}"
                    sh 'taskcat test run'
                    echo 'Finished Infrastructure Tests'
                }
            }
        }
        stage('Deploy') {
            steps {
                withEnv(['PATH+EXTRA=/usr/local/bin']) {
                    echo 'Starting Deployment'
                    sh "python3 scripts/deploy.py --StackName ${env.AQS_STACK_NAME} --S3GlueBucketName ${env.AQS_S3_GLUE_BUCKET_NAME} --S3RawDataBucketName ${env.AQS_S3_RAW_DATA_BUCKET_NAME} --S3ProcessedDataBucketName ${env.AQS_S3_PROCESSED_DATA_BUCKET_NAME} --S3AthenaBucketName ${env.AQS_S3_ATHENA_BUCKET_NAME} --S3GlueScriptsBucketName ${env.AQS_S3_GLUE_SCRIPTS_BUCKET_NAME}"
                    echo 'Finished Deployment'
                }
            }
        }
    }
}