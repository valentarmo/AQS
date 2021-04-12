pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
    }
    stages {
        stage('Test Stack') {
            steps {
                withEnv(['PATH+EXTRA=/usr/local/bin']) {
                    echo 'Starting Infrastructure Tests'
                    sh "python3 scripts/create-taskcat-file.py --Region ${env.AWS_DEFAULT_REGION} --S3BucketPrefix ${env.AQS_S3_BUCKET_PREFIX}"
                    sh 'taskcat test run'
                    echo 'Finished Infrastructure Tests'
                }
            }
        }
        stage('Deploy') {
            steps {
                withEnv(['PATH+EXTRA=/usr/local/bin']) {
                    echo 'Starting Deployment'
                    sh "python3 scripts/deploy.py --StackName ${env.AQS_STACK_NAME} --S3BucketPrefix ${env.AQS_S3_BUCKET_PREFIX}"
                    echo 'Finished Deployment'
                }
            }
        }
    }
}