pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}/venv"
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
                    // Crear virtualenv si no existe
                    if (!fileExists("${env.VENV_DIR}/Scripts/activate")) {
                        bat "python -m venv ${env.VENV_DIR}"
                    }
                    // Instalar dependencias
                    bat """
                    ${env.VENV_DIR}\\Scripts\\pip install --upgrade pip
                    ${env.VENV_DIR}\\Scripts\\pip install -r requirements.txt
                    """
                }
            }
        }

        stage('Format with Black') {
            steps {
                script {
                    // Formatear todo el proyecto
                    bat "${env.VENV_DIR}\\Scripts\\python -m black . --check"
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Solo si tienes tests configurados
                    // bat "${env.VENV_DIR}\\Scripts\\pytest tests/"
                    echo "No hay tests definidos aún"
                }
            }
        }
    }

    post {
        success {
            echo 'Build y formateo completados correctamente.'
        }
        failure {
            echo 'Error en el pipeline. Revisar la consola para detalles.'
        }
    }
}
