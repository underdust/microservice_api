pipeline {
    agent any
    
    environment {
        DOCKER_CREDS_ID = 'dockerhub-credentials' 
        DOCKER_IMAGE = 'underdust/microservice-api' 
        TAG = 'latest'
        REPO2_URL = 'https://github.com/underdust/microservice_robot_test.git'
    }

    stages {
        stage('Unit Test (FastAPI)') {
            steps {
                echo 'Running Unit Tests for mul10...'
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                pytest test_main.py -v
                '''
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                echo 'Building and pushing Docker image to Registry...'
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${TAG} ."
                    
                    withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDS_ID, passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER')]) {
                        sh "echo \$DOCKER_PASS | docker login -u \$DOCKER_USER --password-stdin"
                        sh "docker push ${DOCKER_IMAGE}:${TAG}"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to K8s Cluster...'
                sh 'kubectl apply -f k8s/deployment.yaml --insecure-skip-tls-verify'
                sh 'kubectl apply -f k8s/service.yaml --insecure-skip-tls-verify --validate=false'
                sh 'kubectl rollout restart deployment fastapi-microservice --insecure-skip-tls-verify'
                
                echo 'Waiting for rollout to complete...'
                sh 'kubectl rollout status deployment fastapi-microservice --insecure-skip-tls-verify'
            }
        }

        stage('Robot Framework Test') {
            steps {
                echo 'Cloning Repo 2 and running Robot Framework...'
                sh 'rm -rf robot_tests' 
                sh 'git clone ${REPO2_URL} robot_tests'
                sh '''
                . venv/bin/activate
                nohup uvicorn main:app --host 0.0.0.0 --port 8000 > api.log 2>&1 &
                sleep 5
                pip install -r robot_tests/requirements.txt
                # รัน robot และเก็บผลลัพธ์ไว้ที่ระดับ root เพื่อให้ plugin หาเจอ
                robot --outputdir . robot_tests/test_mul10.robot || true
                '''
            }
            post {
                always {
                    step([$class: 'RobotPublisher',
                        outputPath: '.',
                        outputFileName: 'output.xml',
                        reportFileName: 'report.html',
                        logFileName: 'log.html',
                        disableArchiveResults: false,
                        passThreshold: 100.0,
                        unstableThreshold: 80.0
                    ])
                    sh 'pkill -f uvicorn || true'
                    sh 'rm -rf robot_tests' 
                }
            }
        }
    }
}