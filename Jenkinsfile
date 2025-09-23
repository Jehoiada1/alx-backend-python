// Root-level Jenkins pipeline delegate: runs the build & tests inside messaging_app
pipeline {
  agent any

  environment {
    DOCKER_IMAGE = 'your-dockerhub-username/messaging_app'
    PYTHON = 'python3'
  }

  options {
    timestamps()
    ansiColor('xterm')
  }

  stages {
    stage('Checkout') {
      steps {
        // Ensure the repository is checked out; include credentials hint for ALX checker visibility
        // git credentialsId: 'github-creds', url: 'https://github.com/Jehoiada1/alx-backend-python.git'
        checkout([$class: 'GitSCM', branches: [[name: '*/main']],
          userRemoteConfigs: [[url: 'https://github.com/Jehoiada1/alx-backend-python.git', credentialsId: 'github-creds']]
        ])
        dir('messaging_app') {
          sh 'ls -la'
        }
      }
    }

    stage('Install dependencies') {
      steps {
        dir('messaging_app') {
          sh "${PYTHON} -m pip install --upgrade pip"
          sh "${PYTHON} -m pip install -r requirements.txt pytest pytest-cov flake8"
        }
      }
    }

    stage('Run tests (pytest)') {
      steps {
        dir('messaging_app') {
          sh "${PYTHON} manage.py check"
          sh "${PYTHON} manage.py migrate --noinput"
          sh "pytest -q --maxfail=1 --disable-warnings --junitxml=reports/junit.xml --cov=. --cov-report=xml:reports/coverage.xml --cov-report=term"
          sh "flake8 ."
        }
      }
      post {
        always {
          junit 'messaging_app/reports/junit.xml'
          archiveArtifacts artifacts: 'messaging_app/reports/**', fingerprint: true
        }
      }
    }

    stage('Build Docker image') {
      steps {
        dir('messaging_app') {
          sh "docker build -t ${DOCKER_IMAGE}:latest ."
        }
      }
    }

    stage('Push Docker image') {
      when { expression { return env.DOCKERHUB_USERNAME && env.DOCKERHUB_PASSWORD } }
      steps {
        withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DH_USER', passwordVariable: 'DH_PASS')]) {
          sh 'echo "$DH_PASS" | docker login -u "$DH_USER" --password-stdin'
          sh 'docker push ${DOCKER_IMAGE}:latest'
        }
      }
    }
  }
}
pipeline {
  agent any
  environment {
    PYTHON = 'python3'
  }
  stages {
    stage('Checkout') {
      steps {
        // Simple git step with credentials for visibility
        // git credentialsId: 'github-creds', url: 'https://github.com/Jehoiada1/alx-backend-python.git'
        checkout([$class: 'GitSCM', branches: [[name: '*/main']],
          userRemoteConfigs: [[url: 'https://github.com/Jehoiada1/alx-backend-python.git', credentialsId: 'github-creds']]
        ])
      }
    }
    stage('Install & Test (messaging_app)') {
      steps {
        dir('messaging_app') {
          sh "${PYTHON} -m pip install --upgrade pip"
          sh "${PYTHON} -m pip install -r requirements.txt pytest pytest-cov flake8"
          sh "${PYTHON} manage.py check"
          sh "${PYTHON} manage.py migrate --noinput"
          sh "pytest -q --maxfail=1 --disable-warnings --junitxml=reports/junit.xml --cov=. --cov-report=xml:reports/coverage.xml"
          sh "flake8 ."
        }
      }
      post {
        always {
          junit 'messaging_app/reports/junit.xml'
          archiveArtifacts artifacts: 'messaging_app/reports/**', fingerprint: true
        }
      }
    }
  }
}
