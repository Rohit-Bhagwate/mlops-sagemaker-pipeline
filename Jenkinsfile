pipeline {
    agent any

    stages {

        stage('Checkout Verification') {
            steps {
                echo 'GitHub checkout successful'
            }
        }

        stage('Python Verification') {
            steps {
                sh 'python3 --version'
                sh 'whoami'
                sh 'pwd'
            }
        }
    }
}