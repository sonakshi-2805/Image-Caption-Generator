pipeline {
    agent any

    stages {

        stage('Docker Version') {
            steps {
                sh 'docker --version'
            }
        }

        stage('Docker Compose Version') {
            steps {
                sh 'docker compose version'
            }
        }

        stage('Build Docker Images') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Stop Old Containers') {
            steps {
                sh 'docker compose down'
            }
        }

        stage('Start Containers') {
            steps {
                sh 'docker compose up -d'
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'docker ps'
            }
        }
    }
}
