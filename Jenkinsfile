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
                        file: 'model_artifact.txt'
                    ).trim()

                    echo "Model artifact: ${env.MODEL_ARTIFACT}"
                }
            }
        }

        stage('Prepare Inference Code') {
            steps {
                sh '''
                    echo "Preparing inference code outside Jenkins workspace..."

                    rm -rf /tmp/telecom-churn-inference-code

                    cp -R training/inference_code \
                        /tmp/telecom-churn-inference-code

                    echo "Inference code prepared at:"
                    ls -la /tmp/telecom-churn-inference-code
                '''
            }
        }

        stage('Build SageMaker Model') {
            steps {
                sh '''
                    export MODEL_ARTIFACT="${MODEL_ARTIFACT}"
                    export INFERENCE_SOURCE_DIR="/tmp/telecom-churn-inference-code"

                    echo "Model artifact:"
                    echo "${MODEL_ARTIFACT}"

                    echo "Inference source directory:"
                    echo "${INFERENCE_SOURCE_DIR}"

                    .venv/bin/python training/sagemaker_model.py
                '''
            }
        }

        stage('Cleanup Temporary Files') {
            steps {
                sh '''
                    rm -rf /tmp/telecom-churn-inference-code
                    echo "Temporary inference directory cleaned."
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline execution completed.'
        }
    }
}
