Pipeline {
    agent any
    environment {
        STACK_NAME = 'DataLakeStack'
        PREFIX = 'valentarmo'
    }
    stages {
        stage('Test Stack') {
            steps {
                echo 'Starting Tests...'
                sh 'taskcat test run'
                echo 'Finished Tests...'
            }
        }
        stage('Create Or Update Stack') {
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                echo 'Starting Stack Deployment...'
                script {
                    withAWS(profile: 'myProfile') {
                        def outputs = cfnUpdate(stack: '${env.STACK_NAME}', file: 'templates/DataLake.yaml', params:['Prefix=${env.PREFIX}'])
                        env.SCRIPTS_BUCKET_NAME = outputs['ScriptsBucketName']
                        echo 'Output: ${outputs}'
                    }
                }
                echo 'Finished Stack Deployment...'
            }
        }
        stage('Upload ETL Script') {
            when {
                expression {
                    currentBuild.result == null || currentBuild.result == 'SUCCESS'
                }
            }
            steps {
                echo 'Starting Script Uploading...'
                script {
                    withAWS(profile: 'myProfile') {
                        s3Upload(file: 'scripts/AirQualityToColumnarFormatHourly.py', bucket:'${env.SCRIPTS_BUCKET_NAME}', path:'/')
                    }
                }
                echo 'Finished Script Uploading...'
            }
        }
    }
}