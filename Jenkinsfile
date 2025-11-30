pipeline {
    agent any

    tools {
        maven 'MAVEN-3'   // My maven name
    }

    parameters {
        booleanParam(
            name: 'executeTests',
            defaultValue: true,
            description: 'Run the Test stage?'
        )
    }

    environment {
        VERSION = "1.0.0"
        ENVIRONMENT_NAME = "Development"
    }

    stages {

        stage('Build') {
            steps {
                echo "Building version: ${VERSION}"
                echo "Environment: ${ENVIRONMENT_NAME}"

                // Show Maven version (Windows uses bat instead of sh)
                bat "mvn --version"
            }
        }

        stage('Test') {
            when {
                expression {
                    return params.executeTests == true
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
            echo 'Post Action if build failed'
        }
    }
}
