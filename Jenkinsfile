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
    }
}
