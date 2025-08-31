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
                    try {
                        if (!fileExists("${env.VENV_DIR}\\Scripts\\activate")) {
                            bat "python -m venv ${env.VENV_DIR}"
                        }

                        bat """
                        ${env.VENV_DIR}\\Scripts\\python.exe -m pip install --upgrade pip
                        ${env.VENV_DIR}\\Scripts\\python.exe -m pip install -r requirements2.txt
                        """

                    } catch (err) {
                        error "Error al configurar virtualenv o instalar dependencias: ${err}"
                    }
                }
            }
        }

        stage('Format with Black') {
            steps {
                script {
                    try {
                        bat "${env.VENV_DIR}\\Scripts\\python -m black . --check"
                    } catch (err) {
                        echo "Advertencia: Black detectó problemas de formato."
                    }
                }
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
