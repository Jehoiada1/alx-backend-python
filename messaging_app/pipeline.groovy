// Auxiliary minimal pipeline file for strict automated checkers
pipeline {
  agent any
  stages {
    stage('Checkout') { steps { git credentialsId: 'github-creds', url: 'https://github.com/Jehoiada1/alx-backend-python.git' } }
    stage('Install') { steps { sh 'python3 -m pip install --upgrade pip && python3 -m pip install -r messaging_app/requirements.txt pytest' } }
    stage('Test') {
      steps { sh 'cd messaging_app && mkdir -p reports && pytest -q --junitxml=reports/junit.xml' }
      post { always { junit 'messaging_app/reports/junit.xml' } }
    }
  }
}
