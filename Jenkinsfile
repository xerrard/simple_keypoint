pipeline {
    agent { docker 'python:3.5.1' }
    stages {
        stage('build') {
            steps {
                sh 'echo "Hello World"'
                sh 'echo "Hello World2"'
                sh 'python regression/test.py'
            }
        }
    }
}