pipeline {
    agent any

    environment {
        AWS_ACCESS_KEY_ID = credentials('aws-access-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('aws-secret-access-key')
    }
    stages {
        stage('Test Stack') {
            steps {
                echo 'Starting Infrastructure Tests'
                sh 'python scripts/create-taskcat-file.py --Region ${env.AWS_DEFAULT_REGION} --S3BucketPrefix ${env.AQS_S3_BUCKET_PREFIX}'
                sh 'taskcat test run'
                echo 'Finished Infrastructure Tests'
            }
        }
        stage('Deploy') {
            when {
                expression {
                    currentBuild.result == 'SUCCESS'
                } 
            }
            steps {
                echo 'Starting Deployment'
                sh 'pipenv install'
                sh 'pipenv shell'
                sh 'python scripts/deploy.py --StackName ${env.AQS_STACK_NAME} --Region ${evn.AWS_DEFAULT_REGION} --S3BucketPrefix ${env.AQS_S3_BUCKET_PREFIX}'
                sh 'exit'
                echo 'Finished Deployment'
            }
        }
    }
}