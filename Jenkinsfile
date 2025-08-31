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
                    ${env.VENV_DIR}\\Scripts\\python.exe -m pip install --upgrade pip
                    ${env.VENV_DIR}\\Scripts\\python.exe -m pip install -r requirements.txt
                    """
                }
            }
        }

        stage('Format with Black') {
            steps {
                script {
                    // Ejecuta Black y captura el código de salida
                    def status = bat(script: "${env.VENV_DIR}\\Scripts\\python -m black . --check", returnStatus: true)

                    if (status != 0) {
                        // Falla el build si Black detecta problemas
                        error("Black detectó problemas de formato. Por favor ejecuta 'black .' para formatear el código antes de hacer commit.")
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
