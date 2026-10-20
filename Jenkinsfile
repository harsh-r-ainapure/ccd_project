
pipeline {
    agent any

    environment {
        AWS_REGION     = 'ap-south-1'
        ECR_REPOSITORY = 'image-regi'
        IMAGE_NAME     = 'cloud-image'
        AWS_ACCOUNT_ID = '424683027930'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Test') {
            steps {
                sh '''
                    set -e

                    echo "Checking Python installation..."
                    python3 --version

                    echo "Checking application syntax..."
                    python3 -m py_compile app.py

                    if [ -f requirements.txt ]; then
                        echo "Installing Python dependencies..."
                        python3 -m venv .venv
                        .venv/bin/python -m pip install --upgrade pip
                        .venv/bin/python -m pip install -r requirements.txt
                    else
                        echo "No requirements.txt found; skipping dependency installation."
                    fi

                    echo "Python checks completed successfully."
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    set -e
                    docker build -t ${IMAGE_NAME}:latest .
                '''
            }
        }

        stage('ECR Login') {
            steps {
                sh '''
                    set -e

                    ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

                    aws ecr get-login-password \
                        --region "${AWS_REGION}" |
                    docker login \
                        --username AWS \
                        --password-stdin "${ECR_REGISTRY}"
                '''
            }
        }

        stage('Docker Tag') {
            steps {
                sh '''
                    set -e

                    ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

                    docker tag \
                        ${IMAGE_NAME}:latest \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    set -e

                    ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

                    docker push \
                        ${ECR_REGISTRY}/${ECR_REPOSITORY}:latest
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully! Docker image pushed to ECR.'
        }

        failure {
            echo 'Pipeline failed. Check the Jenkins console output.'
        }

        always {
            echo 'Jenkins pipeline execution finished.'
        }
    }
}
