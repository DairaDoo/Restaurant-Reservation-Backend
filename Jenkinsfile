pipeline {
    agent any

    environment {
        VENV_DIR = "${WORKSPACE}\\venv"
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

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
                    def status = bat(script: "${env.VENV_DIR}\\Scripts\\python -m black . --check", returnStatus: true)

                    if (status != 0) {
                        error("Black detectó problemas de formato. Por favor ejecuta 'black .' para formatear el código antes de hacer commit.")
                    }
                }
            }
        }

        stage('Run Tests with Coverage') {
            steps {
                script {
                    bat """
                    ${env.VENV_DIR}\\Scripts\\python.exe -m pytest ^
                        --cov=app ^
                        --cov-report=xml ^
                        --cov-report=html ^
                        --cov-report=term-missing ^
                        --junitxml=test-results\\results.xml
                    """
                }
            }
        }

        stage('Publish Reports') {
            steps {
                // Publica cobertura en Jenkins (Coverage Plugin)
                recordCoverage tools: [cobertura('coverage.xml')]

                // Publica resultados de tests (JUnit)
                junit 'test-results/results.xml'

                // Archiva el reporte HTML de coverage
                archiveArtifacts artifacts: 'htmlcov/**', fingerprint: true
            }
        }

    }

    post {
        success {
            echo '✅ Build, formato y tests completados correctamente.'
        }
        failure {
            echo '❌ Pipeline falló. Revisar la salida de consola.'
        }
    }
}
