```groovy
pipeline {
    agent any

    environment {
        // AWS region is controlled by the Jenkins environment
        AWS_DEFAULT_REGION = 'ap-south-1'
        AWS_REGION = 'ap-south-1'
    }

    stages {

        stage('Checkout Verification') {
            steps {
                echo 'GitHub checkout successful'
            }
        }

        stage('Python Verification') {
            steps {
                sh '''
                    python3 --version
                    whoami
                    pwd

                    echo "AWS Region:"
                    echo $AWS_DEFAULT_REGION
                '''
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

        stage('Verify Dependencies') {
            steps {
                sh '''
                    .venv/bin/python -c "import boto3; print('boto3:', boto3.__version__)"
                    .venv/bin/python -c "import sagemaker; print('SageMaker SDK imported successfully')"
                    .venv/bin/python -c "import sklearn; print('scikit-learn:', sklearn.__version__)"
                    .venv/bin/python -c "import joblib; print('joblib:', joblib.__version__)"
                '''
            }
        }

        stage('Verify AWS Access') {
            steps {
                sh '''
                    echo "Testing AWS identity..."
                    aws sts get-caller-identity

                    echo "Testing AWS region..."
                    aws configure get region || true
                '''
            }
        }

        stage('Verify Project Files') {
            steps {
                sh '''
                    echo "Project files:"
                    find training src -maxdepth 3 -type f | sort

                    echo "Checking SageMaker training script:"
                    test -f training/sagemaker_train.py

                    echo "Checking test input JSON:"
                    test -f training/test_input.json

                    echo "Checking inference code:"
                    test -f training/inference_code/inference.py

                    echo "All required project files are present."
                '''
            }
        }

        stage('Run SageMaker Training') {
            steps {
                sh '''
                    .venv/bin/python training/sagemaker_train.py
                '''
            }
        }

        stage('Read Model Artifact') {
            steps {
                script {
                    env.MODEL_ARTIFACT = readFile(
                        'model_artifact.txt'
                    ).trim()

                    echo "Model artifact: ${env.MODEL_ARTIFACT}"
                }
            }
        }

        stage('Build SageMaker Model') {
            steps {
                sh '''
                    echo "Building SageMaker model..."

                    .venv/bin/python training/sagemaker_model.py
                '''
            }
        }
    }
}
```
