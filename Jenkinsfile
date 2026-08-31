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

        stage('Create Python Environment') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python --version
                    .venv/bin/pip --version
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }
    }
}