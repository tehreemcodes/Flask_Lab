pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                echo 'Building...'
            }
        }

        stage('Test') {
            when {
                expression {
                    // Condition: run tests only if this returns true
                    return true
                }
            }
            steps {
                echo 'Testing...'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying....'
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
