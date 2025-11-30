pipeline {
    agent any

    environment {
        VERSION = "1.0.0"
        ENVIRONMENT_NAME = "Development"
    }

    stages {

        stage('Build') {
            steps {
                echo "Building version: ${VERSION}"
                echo "Environment: ${ENVIRONMENT_NAME}"
            }
        }

        stage('Test') {
            when {
                expression {
                    return true
                }
            }
            steps {
                echo 'Testing...'
            }
        }

        stage('Deploy') {
            steps {
                echo "Deploying version ${VERSION} to ${ENVIRONMENT_NAME}"
            }
        }
    }

    post {
        always {
            echo 'Post build condition running'
        }
        failure {
            echo 'Post Action if build Failed'
        }
    }
}
