pipeline {
    // Usamos un agente Docker con Python 3.9
    agent {
        docker {
            image 'python:3.9-slim'
            args '-u'  // para output en tiempo real
        }
    }

    environment {
        VENV_DIR = "${WORKSPACE}/venv"
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Obteniendo código desde GitHub...'
                git branch: 'main',
                    url: 'https://github.com/DairaDoo/Restaurant-Reservation-Backend.git',
                    credentialsId: 'DairaDoo'
            }
        }

        stage('Setup Virtual Environment & Install Dependencies') {
            steps {
                script {
                    echo 'Instalando dependencias...'
                    // Creamos el virtualenv
                    sh """
                    python -m venv ${VENV_DIR}
                    source ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    """
                }
            }
        }

        stage('Code Formatting with Black') {
            steps {
                script {
                    echo 'Revisando formato con Black...'
                    sh """
                    source ${VENV_DIR}/bin/activate
                    python -m black . --check
                    """
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Ejecutando tests (si existen)...'
                    // Aquí podrías usar pytest si tienes tests
                    // sh "source ${VENV_DIR}/bin/activate && pytest tests/"
                    echo "No hay tests definidos aún"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completado correctamente: Código formateado y dependencias instaladas.'
        }
        failure {
            echo 'Pipeline falló. Revisar la salida de consola para más detalles.'
        }
    }
}
