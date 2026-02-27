pipeline {
    agent any

    environment {
        DOCKER_CREDS_ID  = 'dockerhub-credentials'
        DOCKER_IMAGE     = 'underdust/microservice-api'
        TAG              = 'latest'
        REPO2_URL        = 'https://github.com/underdust/microservice_robot_test.git'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Unit Test (mul10 only)') {
            steps {
                echo 'Running Unit Tests for mul10...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    mkdir -p test-results
                    pytest test_main.py -v --junitxml=test-results/results.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results/*.xml'
                }
            }
        }

        stage('Robot Framework Test (mul10 only)') {
            steps {
                echo 'Cloning Repo 2 and running Robot Framework tests...'
                sh 'git clone ${REPO2_URL} robot_tests'
                sh '''
                    . venv/bin/activate
                    nohup uvicorn main:app --host 0.0.0.0 --port 8000 > api.log 2>&1 &
                    sleep 5
                    pip install -r robot_tests/requirements.txt
                    robot --outputdir robot_results robot_tests/test_mul.robot
                '''
            }
            post {
                always {
                    sh 'pkill -f uvicorn || true'
                    sh 'rm -rf robot_tests'
                    archiveArtifacts artifacts: 'robot_results/**', allowEmptyArchive: true
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                echo 'Building Docker image...'
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${TAG} ."
                    withCredentials([usernamePassword(
                        credentialsId: env.DOCKER_CREDS_ID,
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )]) {
                        sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
                        sh "docker push ${DOCKER_IMAGE}:${TAG}"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes cluster...'
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
                sh 'kubectl rollout status deployment/fastapi-microservice'
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}