pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}\\venv"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/DairaDoo/Restaurant-Reservation-Backend.git',
                    credentialsId: 'DairaDoo'
            }
        }

        stage('Setup Virtualenv & Install Dependencies') {
            steps {
                script {
                    if (!fileExists("${env.VENV_DIR}\\Scripts\\activate")) {
                        bat "python -m venv ${env.VENV_DIR}"
                    }

                    bat """
                    ${env.VENV_DIR}\\Scripts\\pip install --upgrade pip
                    ${env.VENV_DIR}\\Scripts\\pip install -r requirements.txt
                    """
                }
            }
        }

        stage('Format with Black') {
            steps {
                bat "${env.VENV_DIR}\\Scripts\\python -m black . --check"
            }
        }

        stage('Run Tests') {
            steps {
                echo "No hay tests definidos aún"
            }
        }
    }

    post {
        success {
            echo 'Build y formateo completados correctamente.'
        }
        failure {
            echo 'Pipeline falló. Revisar la salida de consola.'
        }
    }
}
