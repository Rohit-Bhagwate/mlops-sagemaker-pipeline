pipeline {
    agent any

    environment {
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
                    echo "$AWS_DEFAULT_REGION"

                    echo "AWS Identity:"
                    aws sts get-caller-identity
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

                    echo "Checking SageMaker model script:"
                    test -f training/sagemaker_model.py

                    echo "Checking Endpoint Configuration script:"
                    test -f training/sagemaker_endpoint_config.py

                    echo "Checking Endpoint script:"
                    test -f training/sagemaker_endpoint.py

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
                    def artifact = readFile(
                        file: 'model_artifact.txt'
                    ).trim()

                    echo "Model artifact:"
                    echo artifact

                    env.MODEL_ARTIFACT = artifact
                }
            }
        }

        stage('Prepare Inference Code') {
            steps {
                sh '''
                    rm -rf "/tmp/telecom-churn-inference-code-${BUILD_NUMBER}"

                    cp -R \
                        training/inference_code \
                        "/tmp/telecom-churn-inference-code-${BUILD_NUMBER}"

                    echo "Inference code staged at:"
                    echo "/tmp/telecom-churn-inference-code-${BUILD_NUMBER}"

                    echo "Contents:"
                    ls -la "/tmp/telecom-churn-inference-code-${BUILD_NUMBER}"
                '''
            }
        }

        stage('Create SageMaker Model') {
            steps {
                sh '''
                    echo "AWS Region: $AWS_DEFAULT_REGION"
                    echo "MODEL_ARTIFACT: $MODEL_ARTIFACT"

                    echo "INFERENCE_SOURCE_DIR:"
                    echo "/tmp/telecom-churn-inference-code-${BUILD_NUMBER}"

                    INFERENCE_SOURCE_DIR="/tmp/telecom-churn-inference-code-${BUILD_NUMBER}" \
                    MODEL_ARTIFACT="$MODEL_ARTIFACT" \
                    .venv/bin/python training/sagemaker_model.py
                '''
            }
        }

        stage('Read Model Name') {
            steps {
                script {
                    def modelName = readFile(
                        file: 'model_name.txt'
                    ).trim()

                    if (!modelName) {
                        error 'model_name.txt is empty.'
                    }

                    echo "SageMaker Model Name:"
                    echo modelName

                    env.MODEL_NAME = modelName
                }
            }
        }

        stage('Create Endpoint Configuration') {
            steps {
                sh '''
                    echo "AWS Region: $AWS_DEFAULT_REGION"
                    echo "SageMaker Model Name: $MODEL_NAME"

                    MODEL_NAME="$MODEL_NAME" \
                    .venv/bin/python training/sagemaker_endpoint_config.py
                '''
            }
        }

        stage('Read Endpoint Configuration Name') {
            steps {
                script {
                    def endpointConfigName = readFile(
                        file: 'endpoint_config_name.txt'
                    ).trim()

                    if (!endpointConfigName) {
                        error 'endpoint_config_name.txt is empty.'
                    }

                    echo "SageMaker Endpoint Configuration Name:"
                    echo endpointConfigName

                    env.ENDPOINT_CONFIG_NAME = endpointConfigName
                }
            }
        }

        stage('Create or Update SageMaker Endpoint') {
            steps {
                sh '''
                    echo "AWS Region: $AWS_DEFAULT_REGION"
                    echo "Endpoint Configuration Name: $ENDPOINT_CONFIG_NAME"

                    ENDPOINT_CONFIG_NAME="$ENDPOINT_CONFIG_NAME" \
                    .venv/bin/python training/sagemaker_endpoint.py
                '''
            }
        }

        stage('Cleanup Temporary Files') {
            steps {
                sh '''
                    rm -rf "/tmp/telecom-churn-inference-code-${BUILD_NUMBER}"
                    rm -f model_artifact.txt
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